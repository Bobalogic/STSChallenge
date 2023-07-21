import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime

# type: units, min, max
SensorUnits = {
    "Temperature": ["Celsius", -10, 45],
    "CO2 level": ["ppm", 100, 1000],
    "Presence": ["Presence", 0, 1],
    "Water meter": ["Liters", 200, 99999999],
    "Gas meter": ["Cubic meters", 4000, 99999999],
    "Noise": ["Decibels", 10, 60],
    "Illuminance": ["Lux", 50, 1000],
    "Electricity meter": ["Watts", 200000, 99999999],
    "Number of people": ["Integer", 0, 800],
}

databaseName = "IoTroopers.db"
dbhub_io_url = "https://dbhub.io/Bobalogic/IoTroopers.db"
existingSensors = {}


def initialize_db():
    try:
        # Connect to SQLite database - this will create a new database file if it doesn't exist
        conn = sqlite3.connect(databaseName, check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute(
            """ SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sensors' """
        )
        # if the count is 1, then table exists
        if cursor.fetchone()[0] == 1:
            print("DB already exists, skipping initialization.")
            # Get all the sensors
            cursor.execute(""" SELECT name, id FROM sensors""")
            sensors = cursor.fetchall()
            # Update the existing sensors
            for sensor in sensors:
                existingSensors.update({sensor[0]: sensor[1]})
        else:
            # Create tables
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS "sensors" (
                    "id" INTEGER PRIMARY KEY,
                    "name" TEXT COLLATE NOCASE,
                    "type" TEXT COLLATE NOCASE,
                    "office" TEXT COLLATE NOCASE,
                    "building" TEXT COLLATE NOCASE,
                    "room" TEXT COLLATE NOCASE,
                    "units" TEXT COLLATE NOCASE
                )
            """
            )

            cursor.execute(
                """
              CREATE TABLE IF NOT EXISTS "sensor_values" (
                "sensor" INTEGER,
                "timestamp" TEXT,
                "value" REAL
              )
            """
            )

            cursor.execute(
                """
                CREATE TRIGGER check_same_sensor
                BEFORE UPDATE ON sensor_values
                FOR EACH ROW
                WHEN NEW.sensor != OLD.sensor
                BEGIN
                    SELECT RAISE(ABORT, 'Sensor ID cannot be changed');
                END;
            """
            )

            # Commit the transaction and close the connection
            conn.commit()

    finally:
        cursor.close()
        conn.close()


'''
def get_sensor_id_from_db():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(databaseName, check_same_thread=False)
        cursor = conn.cursor()

        # Execute a query to get the highest sensor ID from the "sensors" table
        cursor.execute("SELECT MAX(id) FROM sensors")

        # Fetch the result (the maximum sensor ID) from the query
        highest_sensor_id = cursor.fetchone()[0]

        # Close the cursor and connection
        cursor.close()
        conn.close()
        if highest_sensor_id is None:
            return 0
        # Return the highest sensor ID
        return highest_sensor_id

    except sqlite3.Error as e:
        # Handle any potential errors that might occur during the database operation
        print("Error: ", e)
        return None

def add_sensor_to_db(topics):
    new_sensor_id = get_sensor_id_from_db() + 1
    try:
        conn = sqlite3.connect(databaseName, check_same_thread=False)
        cursor = conn.cursor()
        # topics: Office, Building, Room, Name, Type, Units
        cursor.execute("""
            INSERT INTO sensors (id, name, type, office, building, room, units) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (new_sensor_id, topics[3], topics[4], topics[0], topics[1], topics[2], topics[5]))

        conn.commit()

    except sqlite3.Error as e:
        # Handle any potential errors that might occur during the database operation
        print("Error: ", e)

    finally:
        cursor.close()
        conn.close()
    return new_sensor_id
'''


def get_current_timestamp():
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_timestamp


def add_sensor_value_to_db(id, value):
    try:
        conn = sqlite3.connect(databaseName, check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO sensor_values (sensor, timestamp, value) VALUES (?, ?, ?)
        """,
            (id, get_current_timestamp(), value),
        )

        conn.commit()

    except sqlite3.Error as e:
        # Handle any potential errors that might occur during the database operation
        print("Error: ", e)

    finally:
        cursor.close()
        conn.close()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("SummerCampSTS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # topics: Office, Building, Room, Name, Type, Units
    topics = msg.topic.split("/")[1:]

    # Ignore keepalive messages
    if topics[2] != "keepalive":
        try:
            # Get the match for the sensor unit and it's range of values
            match = SensorUnits.get(topics[-1])
            topics.append(match[0])
            value = int(msg.payload.decode())
            name = topics[3]
            # Check if the value is in a valid range for it's type
            if value < match[1] or value > match[2]:
                print(
                    "Value (", value, ") out of range (", match[1], "-", match[2], ")"
                )
                return
        # If the unit is not recognized
        except TypeError as te:
            print("Error in sensor:", ", ".join(map(str, topics[:-2])))
            print("No known unit for", topics[-1])
            return
        # If it's not an integer value
        except ValueError as ve:
            print("Error in sensor:", ", ".join(map(str, topics[:-2])))
            print("Not a number for value", value)
            return
        # Check if the sensor is in memory
        global existingSensors
        id = existingSensors.get(name, -1)
        # If not, check if it was added to the database
        if id == -1:
            # Verify if the sensor exists
            conn = sqlite3.connect(databaseName, check_same_thread=False)
            cursor = conn.cursor()

            cursor.execute("""SELECT id, name FROM sensors WHERE name = ?;""", (name,))
            queryResult = cursor.fetchone()
            # If it does get it's id and update existingSensors
            if queryResult:
                id = queryResult[0]
                existingSensors.update({name: id})

            cursor.close()
            conn.close()

        # If the sensor is in the database, add the value
        if id != -1:
            add_sensor_value_to_db(id, value)


def start():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", port=1883)
    initialize_db()

    client.loop_forever()


start()
