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

	with st.form(key='form1', clear_on_submit=False):
		id_ = st.number_input("id: ", step=1, min_value=1)
		name_ = st.text_input("name")
		type_ = st.text_input("type")
		office_ = st.text_input("office")
		building_ = st.text_input("building")
		room_ = st.text_input("room")
		units_ = st.text_input("units")
		submit_btn = st.form_submit_button(label="Submit")


	

		if submit_btn:
			if id_ and name_ and type_ and office_ and building_ and room_ and units_:
				headers={
		    		'Content-type':'application/json', 
		    		'Accept':'application/json'
				}
				json_data = {
				    "id": id_,
				    "name": name_,
				    "type": type_,
				    "office": office_,
				    "building": building_,
				    "room": room_,
				    "units": units_
				}

				print(json_data)
				response = requests.post(
					url="http://localhost:5000/sensors",
					headers = headers,
					json=json_data
				)
				

				print(response)
				st.warning(response.text)
			else:
				st.warning("Fill all fields")

	




if selected == 'Sensor Data':
	sensor_id = st.number_input("id: ", step=1, min_value=1)	
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
