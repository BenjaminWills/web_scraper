import pymongo


class Mongo:
    def __init__(self, username: str, password: str, host: str, port: str) -> None:
        self.conn_string = f"mongodb://{username}:{password}@{host}:{port}"
        self.client = self.get_client()

    def get_client(self) -> pymongo.MongoClient:
        return pymongo.MongoClient(self.conn_string)
