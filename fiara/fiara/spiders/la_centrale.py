import scrapy
import unicodedata
from bs4 import BeautifulSoup


class QuotesSpider(scrapy.Spider):
    name = "lacentrale"

    start_urls = [
        "https://www.lacentrale.fr/occasion-voiture-marque-volkswagen.html",
    ]

    def parse_tmp(self, response, **kwargs):
        soup = BeautifulSoup(response.text, features="lxml")
        link_elements = soup.find_all("a", {"class": "searchCard__link"})
        for link_elt in link_elements:
            yield response.follow(link_elt, callback=self.parse_info)

        next_btn = soup.find("i", {"class": "cbm-picto--arrowR"}).parent
        self.log(next_btn.attrs["href"])
        yield response.follow(next_btn, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, features="lxml")
        link_elements = soup.find_all("a", {"class": "searchCard__link"})
        for link_elt in link_elements:
            yield response.follow(link_elt['href'], callback=self.parse_info)

    def parse_info(self, response):
        soup = BeautifulSoup(response.text, features="lxml")
        self.log("=============================================================================================================")
        car = {
            "announce": response.url,
            "make_model": soup.find("div", {"class": "cbm-title--page"}).get_text().strip(),
            "make_model_detailed": soup.find("h1").get_text().strip(),
            "price": unicodedata.normalize("NFKC", soup.find("span", {"class": "cbm__priceWrapper"}).get_text().strip())
        }
        features_list = soup.find("div", {"class": "cbm-moduleInfos__informationList"}).find_all("li")
        features = dict()
        if features_list is not None:
            for feature in features_list:
                features[feature.span.button.get_text()] = feature.span.next_sibling.get_text()
            car["features"] = features

        self.log(car)

