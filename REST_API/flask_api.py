# By: Manuel Santos
# Run: python .\flask_api.py

from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)


# Request to get specific sensor data
@app.route("/sensors/<sensorId>", methods=["GET"])
def getSensor(sensorId):
    # Connect to database
    db = sqlite3.connect("sensors.db")
    cur = db.cursor()
    # Query database
    res = cur.execute(
        "SELECT value, timestamp FROM sensor_values "
        "WHERE sensor= " + str(sensorId) + " ORDER BY timestamp DESC LIMIT 10"
    )
    result = res.fetchall()
    # Close database connection
    cur.close()
    db.close()
    # Parse result into JSON
    entry = "["
    for read in result:
        subentry = {}
        subentry["value"] = read[0]
        subentry["timestamp"] = read[1]
        entry = entry + json.dumps(subentry) + ","
    entry = entry[:-1] + "]"
    # Return JSON
    return entry


# Request to insert new sensor data
@app.route("/sensors", methods=["POST"])
def addSensor():
    # Get data from request
    data = request.get_json()
    print("Adding sensor " + str(data["id"]))
    # Connect to database
    db = sqlite3.connect("sensors.db")
    cur = db.cursor()
    # Check if sensor exists
    test = cur.execute("SELECT * FROM sensors WHERE id=" + str(data["id"]))
    if test.fetchone() is None:
        # Insert data into database
        cur.execute(
            "INSERT INTO sensors (id, name, type, office, building, room, units)"
            "VALUES (:id, :name, :type, :office, :building, :room, :units)",
            data,
        )
        db.commit()
        # Close database connection
        cur.close()
        db.close()
        return "Sensor " + str(data["id"]) + " added successfully"
    else:
        # Close database connection
        cur.close()
        db.close()
        return "Sensor " + str(data["id"]) + " already exists"


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
