# STS Challenge - IoT Project

## Description

This repository contains the STS Challenge - IoT Project, which demonstrates an IoT system consisting of an IoT sensor data generator, a MQTT broker, a Web Server, and a user interface with a natural language query feature powered by OpenAI's GPT-3.5.

## Components

- **IoT Sensor Data Generator**: Simulates various sensors and publishes generated data to the MQTT broker.
- **MQTT Broker**: Handles communication between the IoT sensor data generator and the Web Server using the Publish-Subscribe architecture.
- **Web Server**: Receives sensor data and provides a REST API for data access. Stores data in a SQLite database.
- **SQLite Database**: Stores sensor data received by the Web Server.
- **User Interface with Natural Language Query Feature**: Incorporates OpenAI's GPT-3.5 for user interaction and natural language queries to retrieve sensor data.

## Setup and Configuration

1. Clone the repository.

2. Install dependencies:

```bash
pip install -r requirements.txt
Generate TLS/SSL certificates and private keys for secure communication between the MQTT broker and the IoT sensor data generator. Place the ca.crt, broker.crt, and broker.key files in the TLS-SSL directory.

Configure the MQTT broker connection settings in the mqtt.py file.

Start the MQTT broker by running the following command:

bash
Copy code
python mqtt.py
Run the Web Server to handle sensor data and API requests:
bash
Copy code
python web_server.py
Access the user interface by opening the provided URL in your web browser.
Usage
Once the setup is complete, the IoT sensor data generator will start publishing simulated sensor data to the MQTT broker. The Web Server will receive this data and store it in the SQLite database. Users can interact with the system through the user interface, accessing sensor data through natural language queries powered by OpenAI's GPT-3.5.

Contributions
Contributions to the STS Challenge - IoT Project are welcome. If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request. Let's work together to make this project even better!

License
This project is licensed under the MIT License.

Acknowledgments
We would like to express our gratitude to OpenAI for providing GPT-3.5, enabling us to implement the natural language query feature in our user interface. Their cutting-edge technology has greatly enhanced the functionality and user experience of this project.
IoTroopers rules!
