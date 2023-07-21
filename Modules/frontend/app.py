import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import requests
import json
from datetime import datetime
import numpy as np
import pandas as pd
from plotly import graph_objs as go

st.set_page_config(page_title="STS APP ")
col1, col2 = st.columns([1, 2])

logo_1 = Image.open("./Modules/frontend/logo_1.png")
logo_2 = Image.open("./Modules/frontend/logo_2.png")
logo_3 = Image.open("./Modules/frontend/logo_3.png")

image = [logo_1, logo_2, logo_3]


def banner(logo_index):
    col1.image(
        image[logo_index], channels="RGB", output_format="auto", use_column_width="auto"
    )
    col2.title("CRITICAL INFORMATION CENTER")
    col2.write("by IoTroopers")


selected = option_menu(
    menu_title=None,
    options=["Add Sensor", "Sensor Data", "GPT"],
    icons=["bell-fill", "box-fill", "chat-text-fill", "Sensors Data"],
    orientation="horizontal",
)

if selected == "Add Sensor":
    banner(1)
    with st.form(key="form1", clear_on_submit=False):
        # id_ = st.number_input("id: ", step=1, min_value=1) increments alone
        name_ = st.text_input("name")
        type_ = st.text_input("type")
        office_ = st.text_input("office")
        building_ = st.text_input("building")
        room_ = st.text_input("room")
        units_ = st.text_input("units")
        submit_btn = st.form_submit_button(label="Submit")

        if submit_btn:
            if name_ and type_ and office_ and building_ and room_ and units_:
                headers = {
                    "Content-type": "application/json",
                    "Accept": "application/json",
                }
                json_data = {
                    # "id": id_,
                    "name": name_,
                    "type": type_,
                    "office": office_,
                    "building": building_,
                    "room": room_,
                    "units": units_,
                }

                print(json_data)
                response = requests.post(
                    url="http://localhost:5000/sensors", headers=headers, json=json_data
                )

                print(response)
                st.warning(response.text)
            else:
                st.warning("Fill all fields")


if selected == "Sensor Data":
    banner(0)
    sensor_id = st.number_input("id: ", step=1, min_value=1)
    if st.button("Send"):
        response = requests.get("http://localhost:5000/sensors/{}".format(sensor_id))

        json_data = json.loads(response.text)

        print(json_data)

        if len(json_data) == 0:  # has no values
            st.warning("Sensor {} has no values".format(sensor_id))

        else:
            st.subheader("Info:")
            st.markdown("**Location :** {}".format(json_data["location"]))
            st.markdown("**Building :** {}".format(json_data["building"]))
            st.markdown("**Room :** {}".format(json_data["room"]))

            time = []
            value = []
            for i in range(10):
                st.write(
                    "Value {} Timestamp: {}".format(
                        json_data["data"][i]["value"],
                        json_data["data"][i]["timestamp"][:-7],
                    )
                )
                datetime_object = datetime.strptime(
                    json_data["data"][i]["timestamp"][:-7], "%Y-%m-%d %H:%M:%S"
                )
                time.append(datetime_object)
                value.append(json_data["data"][i]["value"])

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=time, y=value, name="aaaa"))
            fig.layout.update(
                title_text=json_data["type"],
                xaxis_title="Date",
                yaxis_title=json_data["units"],
            )
            st.plotly_chart(fig)
