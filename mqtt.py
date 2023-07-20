import paho.mqtt.client as mqtt
import sqlite3
from enum import Enum
 
id = 0

# TODO: Add what's left
sensorUnits = {
    'Temperature': 'Celsius',
    'CO2 level': 'ppm',
    'Presence': 'Presence',
    'Water meter': 'Liters',
    'Gas meter': 'Cubic meters'
}

def initialize_db():
    try:
        # Connect to SQLite database - this will create a new database file if it doesn't exist
        conn = sqlite3.connect("IoTroopers.db", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sensors' """)
        #if the count is 1, then table exists
        if cursor.fetchone()[0] == 1:
           print("DB already exists, skipping initialization.")
        else:
            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "sensors" (
                    "id" INTEGER PRIMARY KEY,
                    "name" TEXT COLLATE NOCASE,
                    "type" TEXT COLLATE NOCASE,
                    "office" TEXT COLLATE NOCASE,
                    "building" TEXT COLLATE NOCASE,
                    "room" TEXT COLLATE NOCASE,
                    "units" TEXT COLLATE NOCASE
                )
            """)

            cursor.execute("""
              CREATE TABLE IF NOT EXISTS "sensor_values" (
                "sensor" INTEGER,
                "timestamp" TEXT,
                "value" REAL
              )
            """)

            cursor.execute("""
                CREATE TRIGGER check_same_sensor
                BEFORE UPDATE ON sensor_values
                FOR EACH ROW
                WHEN NEW.sensor != OLD.sensor
                BEGIN
                    SELECT RAISE(ABORT, 'Sensor ID cannot be changed');
                END;
            """)


            # Commit the transaction and close the connection
            conn.commit()

    finally:
        cursor.close()
        conn.close()

'''
def sendToBd(t, value):
    try:
        # Connect to SQLite database - this will create a new database file if it doesn't exist
        conn = sqlite3.connect("IoTroopers.db", check_same_thread=False)
        cursor = conn.cursor()
        global id

        # Add sensor: Office, Building, Room, Name, Type, Units
        # Order: id, name, type, office, building, room, units
        cursor.execute("INSERT INTO sensors VALUES (?,?,?,?,?,?,?)", (id, t[3], t[4], t[0], t[1], t[2], t[5]))
        conn.commit()
        cursor.execute("INSERT INTO sensor_values VALUES (?,?,?)", (id, 'timestamp', value))
        conn.commit()

        print("Added sensor", t[3], " with value", value)

        id += 1
        
    finally:
        cursor.close()
        conn.close()
'''




# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("SummerCampSTS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" --- "+str(msg.payload))
    topics = msg.topic.split('/')[1:]
    topics.append(sensorUnits.get(topics[-1]))
    value = msg.payload.decode()
    # Ignore keepalive messages
    if topics[2] != 'keepalive':
        # topics: Office, Building, Room, Name, Type, Units
        print(topics)
        print(value)
        # TODO: Ready to be stored in db
        #sendToBd(topics, value)

        


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('test.mosquitto.org', port=1883)
initialize_db()


client.loop_forever()
