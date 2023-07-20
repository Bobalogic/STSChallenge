import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import requests
import json
from datetime import datetime

st.set_page_config(page_title="STS APP ")
col1, col2 = st.columns([1,2])

image = Image.open("logo.png")

col1.image(image, channels="RGB", output_format="auto", use_column_width="auto")
col2.title("CRITICAL INFORMATION CENTER")

selected = option_menu(menu_title=None, 
	options=["Add Sensor", "Sensor Data", "GPT"], 
	icons=['bell-fill', 'box-fill', 'chat-text-fill', 'Sensors Data'],
	orientation="horizontal")

if selected == 'Add Sensor':
	if st.button("ADD"):
		headers={
    		'Content-type':'application/json', 
    		'Accept':'application/json'
		}
		json_data = {
		    "id": 1000000,
		    "name": "sensor_name_value",
		    "type": "sensor_type_value",
		    "office": "office_value",
		    "building": "building_value",
		    "room": "room_value",
		    "units": "units_value"
		}

		response = requests.post(
			url="http://localhost:5000/sensors",
			headers = headers,
			json=json_data
		)
		

		print(response)
		st.warning(response.text)




if selected == 'Sensor Data':
	sensor_id = st.text_input("ID:")
	if st.button("Send"):
		response = requests.get("http://localhost:5000/sensors/{}".format(sensor_id))

		json_data = json.loads(response.text)
		#datetime_object = datetime.strptime(json_data[0]['timestamp'][:-7], '%y-%m-%d %H:%M:%S')


		for i in range(10):
			st.write("Value {} Timestamp: {}".format(json_data[i]['value'], json_data[i]['timestamp'][:-7]))

if selected == 'GPT':
	prompt = st.text_input("enter your question")
	if st.button("Send"):
		response = requests.post("http://localhost:5000/nlquery/{}".format(prompt))
		st.warning(response.text)
