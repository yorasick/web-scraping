import json

class ParserBase:
    def __init__(self, output_file):
        self.output_file = output_file


    def parse_list(self, max_page: int):
        page = 1
        while page <= max_page:
            products = self.parse_page(page)
            if len(products) == 0:
                break
            yield products
            page += 1


    def write_to_json(self, data):
        with open(self.output_file, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)