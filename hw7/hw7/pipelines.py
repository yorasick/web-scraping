# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class Hw7Pipeline:
    def open_spider(self, spider):
        filename = 'quotes.db'
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                author TEXT NOT NULL
            )
        """)
        self.connection.commit()

    
    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO quotes (text, author) VALUES (?, ?)
        """, (item['text'], item['author']))
        self.connection.commit()
        return item
