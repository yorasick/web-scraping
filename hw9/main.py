import json
from OkWine import OkWineParser
from GoodWine import GoodWineParser
from WineTime import WineTimeParser

if __name__ == "__main__":
    # parser = OkWineParser()
    # output_file = 'OkWine.json'

    # parser = GoodWineParser()
    # output_file = 'GoodWine.json'

    parser = WineTimeParser()
    output_file = 'WineTime.json'

    result = []
    for products in parser.parse_whisky_list(max_page=1):
        result.extend(products)

    # TODO: save to db
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
