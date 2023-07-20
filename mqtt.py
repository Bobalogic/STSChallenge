import paho.mqtt.client as mqtt
import sqlite3
from enum import Enum
from datetime import datetime

# Tipos de Sensores:
#   - Temperatura = Temperature -> Celsius
#   - CO2 = Gas Meter -> ppm
#   - Presença = Presence -> 0 ou 1
#   - Humidade = Water Meter -> L

#TO DO:
#   - Adicionar os sensores à base de dados
#   - Adicionar os valores dos sensores à base de dados
#   - Dizer à lia para mudar os nomes que usa no MQTT
#   - Fazer a ligação à REST API usando o Flask

#   -Usar a função get_current_timestamp() para obter o timestamp atual

dbhub_io_url = "https://dbhub.io/Bobalogic/IoTroopers.db"

class SensorUnits(Enum):
    Temperature = 'Celsius'
    Gas = 'ppm'
    Presence = 'Presence'
    Water_Meter = 'L'


def initialize_db():
    try:
        # Connect to SQLite database - this will create a new database file if it doesn't exist
        conn = sqlite3.connect("dbhub_io_url", check_same_thread=False)
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

def get_current_timestamp():
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return current_timestamp

def get_sensor_id_from_db():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("dbhub_io_url", check_same_thread=False)
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
    try:
        new_sensor_id = get_sensor_id_from_db() + 1
        conn = sqlite3.connect("dbhub_io_url", check_same_thread=False)
        cursor = conn.cursor()

        sensor_type = topics[4].replace(' ', '_')

        cursor.execute("""
            INSERT INTO sensors (id, name, type, office, building, room, units) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (new_sensor_id, topics[3], topics[2], topics[0], topics[1], topics[4], SensorUnits[sensor_type].value))

        conn.commit()

    except sqlite3.Error as e:
        # Handle any potential errors that might occur during the database operation
        print("Error: ", e)

    finally:
        cursor.close()
        conn.close()

def add_sensor_value_to_db(topics, value):
    try:
        conn = sqlite3.connect("dbhub_io_url", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sensor_values (sensor, timestamp, value) VALUES (?, ?, ?)
        """, (get_sensor_id_from_db(), get_current_timestamp(), value))

        conn.commit()
    
    except sqlite3.Error as e:
        # Handle any potential errors that might occur during the database operation
        print("Error: ", e)

    finally:
        cursor.close()
        conn.close()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("SummerCampSTS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" --- "+str(msg.payload))

    topics = msg.topic.split('/')[1:]
    #print(topics) #representa os parametros do sensor
    #print(msg.payload.decode('utf-8')) #isto é o valor do sensor
    add_sensor_to_db(topics)
    #add_sensor_value_to_db(topics, msg.payload)
    # Office, Building, Room, Sensor Name, Sensor



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('test.mosquitto.org', port=1883)

initialize_db()


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
