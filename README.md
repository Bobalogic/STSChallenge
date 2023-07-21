STS Challenge - IoT Project
This repository contains the STS Challenge - IoT Project, which consists of an IoT sensor data generator serving a MQTT broker connected to a Web Server in a Publish-Subscribe architecture. The Web Server provides a REST API to access the sensor data, which is stored in a SQLite database. Additionally, the project includes a user interface featuring a natural language query feature powered by OpenAI's GPT-3.5.

Description
The project aims to demonstrate a simple yet comprehensive IoT system that involves the following components:

IoT Sensor Data Generator: The IoT sensor data generator simulates various sensors, such as temperature, CO2 level, presence, water meter, gas meter, noise, illuminance, electricity meter, and number of people. The generated data is published to the MQTT broker.

MQTT Broker: The MQTT broker handles the communication between the IoT sensor data generator and the Web Server. It operates on the Publish-Subscribe architecture, allowing sensors to publish data and clients to subscribe to relevant topics.

Web Server: The Web Server is responsible for receiving and storing the sensor data into a SQLite database. It also provides a REST API, allowing users to access the sensor data efficiently.

SQLite Database: The SQLite database stores the sensor data received by the Web Server. It provides a lightweight, self-contained database system for easy data management.

User Interface with Natural Language Query Feature: The user interface allows users to interact with the system. It incorporates OpenAI's GPT-3.5 to enable natural language queries for sensor data retrieval.

Setup and Configuration
To run the STS Challenge - IoT Project locally, follow these steps:

Clone this repository to your local machine.

Install the required dependencies by running the following command:

bash
Copy code
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
