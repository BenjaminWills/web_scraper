import pymongo

from web_scraper.loggers.make_logger import get_logger, make_logging_directory


class Mongo:
    def __init__(self, username: str, password: str, host: str, port: str) -> None:
        self.connection_string = f"mongodb://{username}:{password}@{host}:{port}"
        self.client = self.get_client()

        # CREATING THE LOGGER
        make_logging_directory()
        self.logger = get_logger(
            output_path="logging/mongo.log",
            save_log=True,
            logger_name="Mongo",
        )

    def get_client(self) -> pymongo.MongoClient:
        try:
            client = pymongo.MongoClient(self.connection_string)
            return client
        except pymongo.errors.PyMongoError as pme:
            self.logger.exception(pme)
            return None

    def insert_entry(self, db_name: str, collection: str, entry: dict) -> bool:
        try:
            with self.client as client:
                client.close()
        except pymongo.errors.PyMongoError as pme:
            self.logger.exception(pme)
            return False
