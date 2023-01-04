import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify

app = Flask(__name__)

from web_scraper.database.sql_wrapper import Sql

load_dotenv(override=True)


api_key = os.getenv("api_key")

user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
database = os.getenv("database")

sql = Sql(user, password, host, port, database)


def job_tuple_to_dict(job_tuple: tuple) -> dict:
    keys = (
        "id",
        "title",
        "salary",
        "city",
        "county",
        "position_info",
        "job_description",
    )
    dictionary_contents = zip(keys, job_tuple)
    return dict(dictionary_contents)


@app.route("/find/job", methods=["GET"])
def find_job():
    if request.method == "GET":
        result = sql.execute_query(
            f"""
            SELECT * 
            FROM jobs;
            """
        )
        return jsonify([job_tuple_to_dict(job) for job in result])


@app.route("/find/job/by-id/<int:id>", methods=["GET"])
def find_job_by_id(id: int):
    if request.method == "GET":
        result = sql.execute_query(
            f"""
            SELECT * 
            FROM jobs 
            WHERE id = {id};
            """
        )

        return jsonify(job_tuple_to_dict(tuple(result[0])))
