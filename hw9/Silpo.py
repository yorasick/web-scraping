import requests
from urllib.parse import urljoin

class SilpoParser:
    url = 'https://silpo.ua'
    # default branch id
    branch = '00000000-0000-0000-0000-000000000000'
    api_url = f'https://sf-ecom-api.silpo.ua/v1/uk/branches/{branch}/products'
    

    def __init__(self):
        pass


    def parse_whisky_list(self, max_page: int):
        page = 1
        while page <= max_page:
            products = self.parse_page(page)
            if len(products) == 0:
                break
            yield products
            page += 1


    def parse_page(self, page: int):
        limit = 47
        offset = 47 * (page - 1)
        response = requests.get(self.api_url, params={ 
            "limit": limit, 
            "offset": offset,
            "category": "viski-4466",
            "includeChildCategories": True,
            "sortBy": "popularity",
            "sortDirection": "desc",
            "inStock": False
        }, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        })
        if not response.ok:
            raise Exception(f"Failed to fetch whisky list: {response.status_code} {response.text}")
        else:
            json = response.json()
            product_list = json.get("items", [])
            return [{
                "id": item.get("id", ""),
                "title": item.get("title", ''),
                "url": urljoin(self.url, f"product/{item.get('slug', '')}"),
                "prices": {
                    "price": item.get("price", 0),
                    "old_price": item.get("old_price", 0)
                }
            } for item in product_list]
        