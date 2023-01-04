import os

from dotenv import load_dotenv
from flask import Flask, request

app = Flask(__name__, static_folder="web_scraper")

# from web_scraper.database.sql_wrapper import Sql

load_dotenv(override=True)


api_key = os.getenv("api_key")

user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
database = os.getenv("database")

# sql = Sql(user, password, host, port, database)


@app.route("/find/job-by-id/<int:id>", methods=["GET"])
def find_job_by_id(id: int):
    if request.method == "GET":
        return f"{id}"
