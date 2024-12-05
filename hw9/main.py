import time
from multiprocessing.dummy import Pool

from OkWine import OkWineParser
from GoodWine import GoodWineParser
from WineTime import WineTimeParser
from Silpo import SilpoParser

from ParserBase import ParserBase


def run_parser(parser: ParserBase):
    start_time = time.time()
    print(f"Starting parser: {parser.__class__.__name__}")

    result = []
    for products in parser.parse_list(max_page=1):
        result.extend(products)
    print(f"[{parser.__class__.__name__}]: Found {len(result)} products")
    
    parser.write_to_json(result)
    print(f"[{parser.__class__.__name__}]: Saved products to json:{parser.output_file}")

    exec_time = time.time() - start_time
    print(f"[{parser.__class__.__name__}]: Finished in {exec_time:.2f} seconds")


if __name__ == "__main__":
    parsers: list[ParserBase] = [
        OkWineParser(output_file='OkWine.json'),
        GoodWineParser(output_file='GoodWine.json'),
        WineTimeParser(output_file='WineTime.json'),
        SilpoParser(output_file='Silpo.json')
    ]

    with Pool(len(parsers)) as pool:
        pool.map(run_parser, parsers)
