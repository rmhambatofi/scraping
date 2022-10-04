import os

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "fiara"

    def start_requests(self):
        urls = [
            'https://www.lacentrale.fr'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log('========')
