# diogo mealha
# Python 3.11.4
# using streamlit requests pillow datetime

import streamlit as st
from PIL import Image
import datetime
from funcs import *

st.set_page_config(page_title="STS APP ")

# session state
if '_office_' not in st.session_state:
	st.session_state['_office_'] = "Coimbra"

if '_people_count_' not in st.session_state:
	st.session_state['_people_count_'] = 0

if '_max_capacity_' not in st.session_state:
	st.session_state['_max_capacity_'] = 0

# header
col1, col2 = st.columns([1,2])

image = Image.open("logo.png")

col1.image(image, channels="RGB", output_format="auto", use_column_width="auto")
col2.title("CRITICAL INFORMATION CENTER")

# selectbox
col1_slb, col2_slb = st.columns(2) # equally divided
office = col1_slb.selectbox(label="chose location",options=["Porto", "Coimbra", "Lisboa"], key='_office_',
	on_change=selectbox_callback(st_object=col2_slb, st_state=st.session_state))


st.progress(st.session_state['_people_count_']/st.session_state['_max_capacity_'], text="Capacity")

st.write("Number of workers: ", st.session_state['_people_count_'])
st.write("Max capacity: ", st.session_state['_max_capacity_'])






#st.title("THIS IS THE TITLE")
#info_placeholder = st.empty()
#prompt_bar = st.text_input("enter your input")

#if st.button("SEND"):
	#response = prompt_bar
	#st.warning(body=response)
	##info_placeholder.text = response

#info_placeholder.text = "empty"

#x = st.slider("Select a value")
#st.write(x, "squared is", x * x)
