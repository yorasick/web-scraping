import time
from multiprocessing.dummy import Pool

from db import DatabaseManager
from parsers.OkWine import OkWineParser
from parsers.GoodWine import GoodWineParser
from parsers.WineTime import WineTimeParser
from parsers.Silpo import SilpoParser
from parsers.ParserBase import ParserBase


if __name__ == "__main__":
    db = DatabaseManager('sqlite:///output.db')
    try:
        db.connect()

        parsers: list[ParserBase] = [
            OkWineParser(db),
            GoodWineParser(db),
            WineTimeParser(db),
            SilpoParser(db)
        ]

        with Pool(len(parsers)) as pool:
            pool.map(lambda parser: parser.run(), parsers)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()