# By: Manuel Santos
# Run: python .\flask_api.py

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


# Request to get specific sensor data
@app.route("/sensors/<sensorId>", methods=["GET"])
def getSensor(sensorId):
    db = sqlite3.connect("sensors.db")
    cur = db.cursor()
    res = cur.execute(
        "SELECT value, timestamp FROM sensor_values "
        "WHERE sensor= " + str(sensorId) + " ORDER BY timestamp DESC LIMIT 10"
    )
    result = jsonify(res.fetchone())
    cur.close()
    db.close()
    return result


# Request to insert new sensor data
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


# Request to get sensor values from natural language query
@app.route("/nlquery/<nlquery>", methods=["POST"])
def getQuery(nlquery):
    return "Query the system with prompt -> " + nlquery


# Request to get all rooms in a building
@app.route("/rooms/<building>", methods=["GET"])
def getRoomsInBuilding(building):
    return "Building " + building + " has rooms 1, 2, 3"


# Request to get all buildings in a location
@app.route("/buildings/<location>", methods=["GET"])
def getBuildingsInLocation(location):
    return "Location " + location + " has buildings A, B, C"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
