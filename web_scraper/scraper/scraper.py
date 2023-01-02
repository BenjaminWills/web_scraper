import requests

from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url: str) -> None:
        self.url = url

        # CREATING THE PARSER
        self.parser = self.__get_beautifulsoup_parser()

    def __get_page_info(self) -> bytes:
        page = requests.get(self.url)
        return page.content

    def __get_beautifulsoup_parser(self) -> BeautifulSoup:
        parser = BeautifulSoup(self.__get_page_info(), "html.parser")
        return parser
