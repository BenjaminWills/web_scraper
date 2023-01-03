# Webscraper

In this project Im going to make a webscraper that will scrape a job board periodically and then send each job to a database.

## Database

I will be using postgreSQL as the database of choice. This will be using the [`SQLAlchemy`](https://docs.sqlalchemy.org/en/20/core/engines.html) library. Using the `sql_wrapper` class, I will be able to execute queries directly to the database.

my database runs on:

- port: 5432
- database: scraper
- user: web_scraper
- password: \*\*\*\*
- host: \*\*\*\*

## Scraper

To scrape I have been using the [`beautiful soup`](crummy.com/software/BeautifulSoup/bs4/doc/) library, on [reed.com](reed.com). The code is well documented, so I will not be explaining how it works here.

## Conclusion

The program runs daily, scraping for new jobs on reed.com in a desired location, and then pushing them to a postgreSQL database.
