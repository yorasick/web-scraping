import json
import time
from db import DatabaseManager

class ParserBase:
    name: str = ""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def run(self):
        start_time = time.time()
        print(f"[{self.name}]: Starting parser")

        result = []
        for products in self.parse_list(max_page=1):
            result.extend(products) 
        print(f"[{self.name}]: Found {len(result)} products")
        
        self.write_to_json(result)
        print(f"[{self.name}]: Saved products to json:{self.name}.json")

        self.write_to_db(result)
        print(f"[{self.name}]: Saved products to db")

        exec_time = time.time() - start_time
        print(f"[{self.name}]: Finished in {exec_time:.2f} seconds")
    

    def parse_list(self, max_page: int):
        page = 1
        while page <= max_page:
            products = self.parse_page(page)
            if len(products) == 0:
                break
            yield products
            page += 1


    def write_to_json(self, data):
        with open(self.name + ".json", "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


    def write_to_db(self, data):
        self.db.insert_products(data)