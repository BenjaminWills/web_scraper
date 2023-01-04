import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify

from web_scraper.database.sql_wrapper import Sql

app = Flask(__name__)

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


def validate_api_key(inputted_key: str):
    return inputted_key == api_key


@app.route("/find/job", methods=["GET"])
def find_job():
    inputted_key = str(request.args.get("api-key"))
    if validate_api_key(inputted_key):
        if request.method == "GET":
            result = sql.execute_query(
                f"""
                SELECT * 
                FROM jobs;
                """
            )
            return jsonify([job_tuple_to_dict(job) for job in result])
    else:
        return jsonify(dict(error=404))


@app.route("/find/job/by-id/<int:id>", methods=["GET"])
def find_job_by_id(id: int):
    inputted_key = str(request.args.get("api-key"))
    if validate_api_key(inputted_key):
        if request.method == "GET":
            result = sql.execute_query(
                f"""
                SELECT * 
                FROM jobs 
                WHERE id = {id};
                """
            )

            return jsonify(job_tuple_to_dict(tuple(result[0])))
    else:
        return jsonify(dict(error=404))
