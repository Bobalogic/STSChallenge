# By: Manuel Santos
# Run: python .\flask_api.py

from flask import Flask, request

# import sqlite3
# conn = sqlite3.connect('sensors.db')
# cur = conn.cursor()

# res = cur.execute("SELECT * FROM sensors")
# print(res.fetchone())

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


@app.route("/rooms/<building>", methods=["GET"])
def getRoomsInBuilding(building):
    return "Building " + building + " has rooms 1, 2, 3"


@app.route("/buildings/<location>", methods=["GET"])
def getBuildingsInLocation(location):
    return "Location " + location + " has buildings A, B, C"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
