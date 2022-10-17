
import scrapy
import unicodedata
from bs4 import BeautifulSoup


class QuotesSpider(scrapy.Spider):
    name = "lacentrale"

    start_urls = [
        "https://www.lacentrale.fr/occasion-voiture-marque-volkswagen.html",
    ]

    # def start_requests(self):
    #     urls = [
    #         'https://www.lacentrale.fr/occasion-voiture.html'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, features="lxml")
        non_break_space = u'\xa0'
        cards = soup.find_all("div", {"class": "searchCard__rightContainer"})
        for card in cards:
            announce = {
                "make_model": card.find("span", {"class": "searchCard__makeModel"}).get_text(),
                "version": card.find("span", {"class": "searchCard__version"}).get_text(),
                "price": unicodedata.normalize("NFKC", card.find("div", {"class": "searchCard__fieldPrice"}).find("span").get_text())
            }
            self.log(announce)
