# By: Manuel Santos
# Run: python .\flask_api.py

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


@app.route("/sensors/<sensorId>", methods=["GET"])
def getSensor(sensorId):
    db = sqlite3.connect("sensors.db")
    cur = db.cursor()
    res = cur.execute("SELECT * FROM sensors WHERE id=" + str(sensorId))
    result = jsonify(res.fetchone())
    cur.close()
    db.close()
    return result


@app.route("/sensors", methods=["POST"])
def addSensor():
    data = request.get_json()
    db = sqlite3.connect("sensors.db")
    cur = db.cursor()
    cur.execute(
        "INSERT INTO sensors (id, name, type, office, building, room, units)"
        "VALUES (:id, :name, :type, :office, :building, :room, :units)",
        data,
    )
    db.commit()
    cur.close()
    db.close()
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
