import requests

from bs4 import BeautifulSoup, element
from web_scraper.loggers.make_logger import get_logger, make_logging_directory

from typing import List
from urllib.error import HTTPError, URLError


class Scraper:
    """
    A scraper for reed.com
    """

    def __init__(self, url: str) -> None:
        self.url = url

        # CREATING THE PARSER
        self.parser = self.__get_beautifulsoup_parser()

        # CREATING THE LOGGER
        make_logging_directory()
        self.logger = get_logger(
            output_path="logging/scraper.log",
            save_log=True,
            logger_name="Scraper",
        )

    def __get_page_info(self) -> bytes:

        try:
            self.logger.info("Loading page information")
            page = requests.get(self.url)
            self.logger.info("Page information loaded")
            return page.content

        except HTTPError or URLError as e:
            self.logger.info("There was an error.")
            self.logger.exception(e)
            return None

    def __get_beautifulsoup_parser(self) -> BeautifulSoup:
        try:
            parser = BeautifulSoup(self.__get_page_info(), "html.parser")
            return parser
        except Exception as e:
            pass

    def find_jobs(self, tag: str, css_class: str) -> List[str]:
        jobs = self.parser.find_all(tag, class_=css_class)
        return jobs

    def __parse_salary(self, salary_tag):
        salary = salary_tag.text.strip()
        return salary

    def __parse_county(self, location_tag):
        county_tag = location_tag.find("span")
        county = county_tag.text.strip()
        return county

    def __parse_location(self, location_tag):
        location_tag_text = location_tag.text
        split_newline = location_tag_text.split("\n")
        location = split_newline[1].strip()
        return location

    def __parse_position(self, position_tag):
        return position_tag.text.strip()

    def __parse_job_title(self, job):
        title_tag = job.find("h2")
        return title_tag.text.strip()

    def __parse_job_description(self, job):
        job_description = job.find("p", {"class": "job-result-description__details"})
        return job_description.text.strip()

    def parse_job(self, job: element.Tag) -> dict:
        list_tags = job.find_all("li")
        salary_tag, location_tag, position_tag = (
            list_tags[0],
            list_tags[1],
            list_tags[2],
        )
        try:
            job_info = {
                "title": self.__parse_job_title(job),
                "salary": self.__parse_salary(salary_tag),
                "city": self.__parse_location(location_tag),
                "county": self.__parse_county(location_tag),
                "position_info": self.__parse_position(position_tag),
                "job_description": self.__parse_job_description(job),
            }
            return job_info
        except Exception as e:
            self.logger.exception(e)
            return None

    def parse_jobs(
        self,
    ) -> List[dict]:
        jobs = self.find_jobs("div", "col-sm-12 col-md-9 details")
        job_dictionaries = [self.parse_job(job) for job in jobs]
        return job_dictionaries
