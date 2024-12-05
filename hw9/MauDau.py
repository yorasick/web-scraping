class MauDauParser:
    url = "https://maudau.ua"

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
        pass