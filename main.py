# TEMP

import streamlit as st
st.write("hellow world")
#st.text_input("Enter text") #returns value that user puts in
#can store it into a variable and use it:
text=st.text_input("Enter text")
st.write(f"the text you entered is: {text}")

#button
is_clicked=st.button("Click me")

#title
st.write("## This is a H2 title!")

st.link_button("name of button", "url to page")