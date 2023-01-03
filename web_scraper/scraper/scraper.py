import requests

from bs4 import BeautifulSoup, element

from typing import List


class Scraper:
    """
    A scraper for reed.com
    """

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

    def find_jobs(self, tag: str, css_class: str) -> List[str]:
        jobs = self.parser.find_all(tag, class_=css_class)
        return jobs

    def parse_job(job: element.Tag) -> dict:
        pass

    def parse_jobs(jobs: List[element.Tag]) -> List[dict]:
        pass
