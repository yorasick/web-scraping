from urllib.parse import urljoin
import requests

from ParserBase import ParserBase


class OkWineParser(ParserBase):
    url = "https://okwine.ua/ua/viski"
    # TODO: make dynamic by category
    api_url = "https://product.okwine.ua/api/v1/filter/products?category=61c460bf1fda1bf332a33c09"


    def __init__(self, output_file):
        super().__init__(output_file)


    def parse_page(self, page: int):
        response = requests.get(self.api_url, params={ "page": page }, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        })
        if not response.ok:
            raise Exception(f"Failed to fetch whisky list: {response.status_code} {response.text}")
        else:
            json = response.json()
            product_list = json.get("data", {}).get("data", [])
            return [{
                "id": item.get("id", ""),
                "title": item.get("name", ''),
                "url": urljoin(self.url, item.get("url", '')),
                "prices": {
                    "price": item.get("prices", {}).get("price", 0),
                    "old_price": item.get("prices", {}).get("old_price", 0)
                }
            } for item in product_list]
