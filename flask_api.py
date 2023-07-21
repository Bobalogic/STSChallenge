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
        "SELECT sensor_values.value, sensor_values.timestamp, sensors.office, sensors.building, sensors.room, sensors.type, sensors.units "
        "FROM sensors INNER JOIN sensor_values "
        "ON sensors.id = sensor_values.sensor "
        "WHERE sensors.id=" + str(sensorId) + " ORDER BY timestamp DESC LIMIT 10"
    )
    result = res.fetchall()
    first = result[0]
    later = [first[2], first[3], first[4], first[5], first[6]]
    # Close database connection
    cur.close()
    db.close()
    # Parse data parameter into JSON
    entry = "["
    for read in result:
        subentry = {}
        subentry["value"] = read[0]
        subentry["timestamp"] = read[1]
        entry = entry + json.dumps(subentry) + ","
    entry = entry[:-1] + "]"
    # Final JSON object
    final = {}
    final["sensor"] = sensorId
    final["location"] = later[0]
    final["building"] = later[1]
    final["room"] = later[2]
    final["type"] = later[3]
    final["units"] = later[4]
    final["data"] = json.loads(entry)
    final = json.dumps(final)
    # Return JSON
    return final


# Request to insert new sensor data
@app.route("/sensors", methods=["POST"])
def addSensor():
    # Get data from request
    data = request.get_json()
    # Connect to database
    db = sqlite3.connect("sensors.db")
    cur = db.cursor()
    # Get most recent sensor value
    max_id = cur.execute("SELECT MAX(id) FROM sensors")
    new_id = max_id.fetchone()[0] + 1
    # Insert data into database
    cur.execute(
        "INSERT INTO sensors (id, name, type, office, building, room, units)"
        "VALUES (" + str(new_id) + ", :name, :type, :office, :building, :room, :units)",
        data,
    )
    db.commit()
    # Close database connection
    cur.close()
    db.close()
    return "Sensor " + str(new_id) + " added successfully"


# Request to get sensor values from natural language query
@app.route("/nlquery/<nlquery>", methods=["POST"])
def getQuery(nlquery):
    return "Query the system with prompt -> " + nlquery


# Request to get all rooms in a building
@app.route("/rooms/<building>/<location>", methods=["GET"])
def getRoomsInBuilding(building, location):
    # Connect to database
    db = sqlite3.connect("sensors.db")
    cur = db.cursor()
    # Query database
    res = cur.execute(
        "SELECT DISTINCT room FROM sensors "
        "WHERE (building= "
        + str(building)
        + "AND office= "
        + str(location)
        + ") ORDER BY room ASC"
    )
    result = res.fetchall()
    print(result)
    # Close database connection
    cur.close()
    db.close()
    # Parse result into JSON
    entry = "["
    # for read in result:
    #     entry = entry + json.dumps(subentry) + ","
    # entry = entry[:-1] + "]"
    # Return JSON
    return entry


# Request to get all buildings in a location
@app.route("/buildings/<location>", methods=["GET"])
def getBuildingsInLocation(location):
    return "Location " + location + " has buildings A, B, C"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
