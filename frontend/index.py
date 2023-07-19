# diogo mealha
# Python 3.11.4
# using streamlit request

import streamlit as st


st.set_page_config(page_title="STS APP teste")

st.title("THIS IS THE TITLE")
#info_placeholder = st.empty()
prompt_bar = st.text_input("enter your input")

if st.button("SEND"):
	response = prompt_bar
	st.warning(body=response)
	#info_placeholder.text = response

info_placeholder.text = "empty"

#x = st.slider("Select a value")
#st.write(x, "squared is", x * x)
