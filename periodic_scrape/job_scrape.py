import os

from web_scraper.database.sql_wrapper import Sql
from web_scraper.scraper.scraper import Scraper
from dotenv import load_dotenv

load_dotenv(override=True)


if __name__ == "__main__":
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port")
    database = os.getenv("database")

    sql = Sql(user, password, host, port, database)

    scraper = Scraper("https://www.reed.co.uk/jobs/jobs-in-SW1A0AA")
    jobs = scraper.parse_jobs()

    sql.insert_jobs_into_table("jobs", jobs)
