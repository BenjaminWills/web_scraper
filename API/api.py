import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify

from web_scraper.database.sql_wrapper import Sql

app = Flask(__name__)

load_dotenv(override=True)

ACCESS_DENIED_CODE = 403

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
        return jsonify(dict(error_code=403))


@app.route("/find/job/by-field/<field>=<value>", methods=["GET"])
def find_job_by_field(field: str, value):
    inputted_key = str(request.args.get("api-key"))
    if validate_api_key(inputted_key):
        if request.method == "GET":
            result = sql.execute_query(
                f"""
                SELECT * 
                FROM jobs 
                WHERE {field} = {value};
                """
            )

            return jsonify(job_tuple_to_dict(tuple(result[0])))
    else:
        return jsonify(dict(error_code=403))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
