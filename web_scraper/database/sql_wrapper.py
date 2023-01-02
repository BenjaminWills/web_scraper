# Base Library

import sqlalchemy
import sys

from web_scraper.loggers.db_logger import make_logging_directory, get_logger

# Error Catching

from sqlalchemy.exc import SQLAlchemyError

# Typing in Functions

from sqlalchemy import engine
from sqlalchemy.engine import LegacyCursorResult


class Sql:
    """
    dialect+driver://username:password@host:port/database - engine connection string.

    A class to wrap SQL alchemy to be used in the webscraper.
    """

    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
    ) -> None:

        # AUTHENTICATION
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        # LOGGING
        make_logging_directory()
        self.logger = get_logger(
            output_path="logging/postgresql.log",
            save_log=True,
            logger_name="SQL Wrapper",
        )

        # ENGINE CREATION
        self.engine = self.get_engine()
        self.logger.info(self._log_connection_credentials())

    def _log_connection_credentials(self) -> str:
        engine_connect_log = f"""
        Successfully connected with credentials:
            Database Username: {self.username}
            Database Password: {'*' * len(self.password)}
            Database Host: {self.host}
            Database Port: {self.port}
            Database Name: {self.database}
        """
        return engine_connect_log

    def get_engine(self) -> engine:
        """Will get the sql engine to connect to the db.

        Returns
        -------
        engine
            Engine that powers the queries.
        """
        connection_string = f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.logger.info("Initalising database engine")
        try:
            engine = sqlalchemy.create_engine(connection_string)
            self.logger.info("Database engine created successfully")
            return engine
        except SQLAlchemyError as sqle:
            self.logger.exception(sqle)
            self.info("Database engine not created")
            sys.exit(0)

    def execute_query(self, query: str) -> LegacyCursorResult:
        """Will execute an inputted postgreSQL query

        Parameters
        ----------
        query : str
            postgreSQL query

        Returns
        -------
        LegacyCursorResult
            result of the query - a tuple.
        """
        try:
            with self.engine.connect() as db_connection:
                result = db_connection.execute(query)
                db_connection.close()
            return result.fetchall()

        except SQLAlchemyError as sqle:
            self.logger.exception(sqle)
            self.logger.info("An error has occured, the query could not be executed.")
            sys.exit(0)
