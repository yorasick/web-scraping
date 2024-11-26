import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    current_page = 0
    max_pages = 1

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            yield {
                "text": quote.xpath(".//span[@class='text']/text()").get(),
                "author": quote.xpath(".//small[@class='author']/text()").get(),
            }

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None and self.current_page < self.max_pages:
            self.current_page += 1
            yield response.follow(next_page, callback=self.parse)
