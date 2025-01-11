# TEMP

# FrontEnd
# Log-in
import streamlit as sl

background_image = """
<style>
[data-testid="stAppViewContainer"] {background-color: #ffffff;
opacity: 1;
background: linear-gradient(135deg, #fffbfc55 25%, transparent 25%) -17px 0/ 34px 34px, linear-gradient(225deg, #fffbfc 25%, transparent 25%) -17px 0/ 34px 34px, linear-gradient(315deg, #fffbfc55 25%, transparent 25%) 0px 0/ 34px 34px, linear-gradient(45deg, #fffbfc 25%, #ffffff 25%) 0px 0/ 34px 34px;
}
</style>
"""
sl.markdown(
    background_image, unsafe_allow_html=True)


sl.write("Log in")
username = sl.text_input("Username")
password = sl.text_input("Password")
if sl.button("Go"):
    sl.switch_page("pages/1_displayoptions.py")
