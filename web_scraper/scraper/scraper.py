import requests

from bs4 import BeautifulSoup

page = requests.get(
    "https://uk.indeed.com/jobs?q=&l=Berkhamsted%2C+Hertfordshire&from=searchOnHP&vjk=edc330f2dc5f7f73"
)


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
