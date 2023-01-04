# Webscraper

In this project have made a webscraper that will scrape a job board periodically and then send each job to a database.

## Database

I will be using postgreSQL as the database of choice. This will be using the [`SQLAlchemy`](https://docs.sqlalchemy.org/en/20/core/engines.html) library. Using the `sql_wrapper` class, I will be able to execute queries directly to the database.

## Scraper

To scrape I have been using the [`beautiful soup`](crummy.com/software/BeautifulSoup/bs4/doc/) library, on [reed.com](reed.com). The code is well documented, so I will not be explaining how it works here.

## API

To query the scraped data for specific jobs I have created an API using [`flask`](https://flask.palletsprojects.com/en/2.2.x/api/).

## Conclusion

The program runs daily, scraping for new jobs on [reed.com](reed.com) in a desired location, and then pushing them to a postgreSQL database.
