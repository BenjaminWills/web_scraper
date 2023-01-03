import requests
import sys

from bs4 import BeautifulSoup, element
from web_scraper.loggers.make_logger import get_logger, make_logging_directory

from typing import List, Dict
from urllib.error import HTTPError, URLError


class Scraper:
    """
    A scraper for reed.com
    """

    def __init__(self, url: str) -> None:
        self.url = url

        # CREATING THE LOGGER
        make_logging_directory()
        self.logger = get_logger(
            output_path="logging/scraper.log",
            save_log=True,
            logger_name="Scraper",
        )

        # CREATING THE PARSER
        self.parser = self.__get_beautifulsoup_parser()

    def __get_page_info(self) -> bytes:
        """Gets the HTML format of the page

        Returns
        -------
        bytes
            page HTML
        """
        try:
            self.logger.info("Loading page information")
            page = requests.get(self.url)
            self.logger.info("Page information loaded")
            return page.content

        except HTTPError or URLError as request_error:
            self.logger.info("There was an error.")
            self.logger.exception(request_error)
            sys.exit(0)

    def __get_beautifulsoup_parser(self) -> BeautifulSoup:
        """Getter for the bs4 parser

        Returns
        -------
        BeautifulSoup
            beautiful soup html parser
        """
        try:
            parser = BeautifulSoup(self.__get_page_info(), "html.parser")
            return parser
        except Exception as e:
            self.logger.info("There was an error.")
            self.logger.exception(e)
            sys.exit(0)

    def find_jobs(self, tag: str, css_class: str) -> List[element.Tag]:
        """gets a list of all of the job listings on a given Reed page.

        Parameters
        ----------
        tag : str
            HTML tag that you are looking for
        css_class : str
            CSS class assosiated with the tag

        Returns
        -------
        List[element.Tag]
            A list of bs4 Tag objects
        """
        try:
            jobs = self.parser.find_all(tag, class_=css_class)
            return jobs
        except Exception as e:
            self.logger.info("There was an error.")
            self.logger.exception(e)
            sys.exit(0)

    def __parse_salary(self, salary_tag: element.Tag) -> str:
        """Parses the salary from a given tag

        Parameters
        ----------
        salary_tag : element.Tag
            Tag containing salary information
        Returns
        -------
        str
            Salary information
        """
        salary = salary_tag.text.strip()
        return salary

    def __parse_county(self, location_tag: element.Tag) -> str:
        """Will parse the county from a location tag

        Parameters
        ----------
        location_tag : element.Tag
            A tag containing the location

        Returns
        -------
        str
            The county
        """
        county_tag = location_tag.find("span")
        county = county_tag.text.strip()
        return county

    def __parse_location(self, location_tag: element.Tag) -> str:
        """Will parse the location (city) from a location tag

        Parameters
        ----------
        location_tag : element.Tag
            A tag containing the location

        Returns
        -------
        str
            city
        """
        location_tag_text = location_tag.text
        split_newline = location_tag_text.split("\n")
        location = split_newline[1].strip()
        return location

    def __parse_position(self, position_tag: element.Tag) -> str:
        """Will parse a position tag to find fulltime, part time etc.

        Parameters
        ----------
        position_tag : element.Tag
            Tag containing position

        Returns
        -------
        str
            posiiton info, i.e full time part time...
        """
        return position_tag.text.strip()

    def __parse_job_title(self, job: element.Tag) -> str:
        """Parses the job tag to find the job title.

        Parameters
        ----------
        job : element.Tag
            Job tag

        Returns
        -------
        str
            Job title
        """
        title_tag = job.find("h2")
        return title_tag.text.strip()

    def __parse_job_description(self, job: element.Tag) -> str:
        """Parses the job for a job description

        Parameters
        ----------
        job : element.Tag
            Job tag

        Returns
        -------
        str
            Job description
        """
        job_description = job.find("p", {"class": "job-result-description__details"})
        return job_description.text.strip()

    def parse_job(self, job: element.Tag) -> Dict[str, str]:
        """parses a job and extracts useful info

        Parameters
        ----------
        job : element.Tag
            Job tag

        Returns
        -------
        Dict[str,str]
            dictionay contianing:
            - title
            - salary
            - city
            - counry
            - position information
            - job description
        """
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
    ) -> List[Dict[str, str]]:
        """Parses all jobs on a webpage

        Returns
        -------
        List[Dict[str, str]]
            A list of summary dictionaries.
        """
        jobs = self.find_jobs("div", "col-sm-12 col-md-9 details")
        job_dictionaries = [self.parse_job(job) for job in jobs]
        return job_dictionaries
