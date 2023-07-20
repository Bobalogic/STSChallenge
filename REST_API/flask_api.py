# By: Manuel Santos
# Run: python .\flask_api.py

from flask import Flask, request

# import sqlite3

app = Flask(__name__)


@app.route("/sensors/<sensorId>", methods=["GET"])
def getSensor(sensorId):
    return "Getting sensor " + sensorId + " data"


@app.route("/sensors", methods=["POST"])
def addSensor():
    return "Adding sensor"


@app.route("/nlquery/<nlquery>", methods=["POST"])
def getQuery(nlquery):
    return "Query the system with prompt -> " + nlquery


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
