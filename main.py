import streamlit as sl
def set_background_from_url(url):
    sl.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{url}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
image_url = "https://i.postimg.cc/FFy83g8R/Untitled-design-2.png"
set_background_from_url(image_url)

sl.title('ShelfConscious')
sl.write('Welcome to ShelfConscious! Please login below.')

username = sl.text_input("Username")
password = sl.text_input("Password")

if sl.button("Login"):
    sl.switch_page("pages/1_displayoptions.py")
