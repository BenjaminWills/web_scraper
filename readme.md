# Webscraper

In this project have made a webscraper that will scrape a job board periodically and then send each job to a database.

## Database

I will be using postgreSQL as the database of choice. This will be using the [`SQLAlchemy`](https://docs.sqlalchemy.org/en/20/core/engines.html) library. Using the `sql_wrapper` class, I will be able to execute queries directly to the database.

## Scraper

To scrape I have been using the [`beautiful soup`](crummy.com/software/BeautifulSoup/bs4/doc/) library, on [reed.com](reed.com). The code is well documented, so I will not be explaining how it works here.

## API

To query the scraped data for specific jobs I have created an API using [`flask`](https://flask.palletsprojects.com/en/2.2.x/api/).

[quickstart reference](https://flask.palletsprojects.com/en/2.2.x/quickstart/#:~:text=To%20run%20the%20application%2C%20use,with%20the%20%2D%2Dapp%20option.&text=As%20a%20shortcut%2C%20if%20the,Line%20Interface%20for%20more%20details.)

## Docker compose

The docker compose file allows a full application deployment by writing the command

```sh
docker compose -f docker-compose.yml up
```

which will start all the services. The services are:

- a `postgreSQL` database (thinking of changing to `mongoDB`)
- an `admin` service for db maintainance, accessible on port `5050`
- a `REST-API` to query the database
- a periodic `web scraper` that will run every day at midnight and scrape new jobs

All of these will be in their own container.

## Conclusion

The program runs daily, scraping for new jobs on [reed.com](reed.com) in a desired location, and then pushing them to a postgreSQL database.

# TODO

- replace `postgres` backend with `mongodb` backend.
