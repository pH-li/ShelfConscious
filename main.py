# TEMP

#<<<<<<< HEAD
# FrontEnd
# Log-in
import streamlit as sl

background_image = """
<style>
[data-testid="stAppViewContainer"] {background-color: #fcfaf6;
opacity: 1;
background: linear-gradient(135deg, #fffbfc55 25%, transparent 25%) 
-17px 0/ 34px 34px, linear-gradient(225deg, #fffbfc 25%, transparent 25%)
 -17px 0/ 34px 34px, linear-gradient(315deg, #fffbfc55 25%, transparent 25%) 
 0px 0/ 34px 34px, linear-gradient(45deg, #fffbfc 25%, #fcfaf6 25%) 0px 0/ 34px 34px;}
</style>
"""
sl.markdown(
    background_image, unsafe_allow_html=True)


sl.write("Log in")
username = sl.text_input("Username")
password = sl.text_input("Password")
if sl.button("Go"):
    sl.switch_page("pages/1_displayoptions.py")
#=======
import streamlit as st
st.write("hellow world")
# st.text_input("Enter text") #returns value that user puts in
# can store it into a variable and use it:
text=st.text_input("Enter text")
st.write(f"the text you entered is: {text}")

# button
is_clicked=st.button("Click me")

# title
st.write("## This is a H2 title!")

st.link_button("name of button", "url to page")
# >>>>>>> a7f8de134cf35935c403227e9dabb1fa76f07ab5
