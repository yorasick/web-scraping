import json
from OkWine import OkWineParser
from GoodWine import GoodWineParser
from WineTime import WineTimeParser
from Silpo import SilpoParser

from ParserBase import ParserBase

if __name__ == "__main__":
    parsers: list[ParserBase] = [
        OkWineParser(output_file='OkWine.json'),
        GoodWineParser(output_file='GoodWine.json'),
        WineTimeParser(output_file='WineTime.json'),
        SilpoParser(output_file='Silpo.json')
    ]

for parser in parsers:
    result = []
    for products in parser.parse_list(max_page=1):
        result.extend(products)

    parser.write_to_json(result)
