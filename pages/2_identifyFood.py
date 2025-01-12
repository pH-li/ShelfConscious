"""
All the data associated with identifying what the user is uploading.
"""

# Import statements
import cv2
import streamlit as st
import numpy as np
from _datetime import datetime

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
st.markdown(
    background_image, unsafe_allow_html=True)

returnHome = st.button(label='Return to Home')

if returnHome:
    st.switch_page("pages/1_displayoptions.py")

st.title('ShelfConscious')
st.write('Welcome! This page is made for you to take or upload pictures of your food. \n'
         'Please make sure to take a clear picture of a single food item you wish to log.'
         ' Press either of the two options below.')

# Initialize session state for tracking mode
if 'upload_mode' not in st.session_state:
    st.session_state.upload_mode = None
if 'frame' not in st.session_state:
    st.session_state.frame = None
if 'picture_taken' not in st.session_state:
    st.session_state.picture_taken = False

# Create placeholders
upload_placeholder = st.empty()
image_placeholder = st.empty()
confirm_placeholder = st.empty()

left_spacer, col1, col2, right_spacer = st.columns([1, 1, 1, 1])

with col1:
    if st.button(label='Take a Picture'):
        st.session_state.upload_mode = 'camera'
        upload_placeholder.empty()
        st.session_state.picture_taken = False

with col2:
    if st.button(label='Upload a Picture'):
        st.session_state.upload_mode = 'upload'
        st.session_state.picture_taken = False

# Handle camera capture
if st.session_state.upload_mode == 'camera':
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        st.session_state.frame = frame
        st.session_state.picture_taken = True
        image_placeholder.image(frame, channels="BGR")
    else:
        st.error("Failed to capture image. Please try again.")

# Handle file upload
if st.session_state.upload_mode == 'upload':
    picture = upload_placeholder.file_uploader("Choose File", type=['jpg', 'jpeg', 'png'])

    if picture is not None:
        file_bytes = np.asarray(bytearray(picture.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)
        if frame is not None:
            st.session_state.frame = frame
            st.session_state.picture_taken = True
            image_placeholder.image(frame, channels="BGR")
        else:
            st.error("Failed to process image. Please try again.")

# Confirmation button
if st.session_state.picture_taken:
    confirmation = confirm_placeholder.button(label='Confirm Picture')
    if confirmation:
        confirm_placeholder.empty()
        upload_placeholder.empty()
        if st.session_state.frame is not None:
            curr_datetime = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            cv2.imwrite('images/' + curr_datetime + '.png', st.session_state.frame)
            st.success("Image saved successfully!")
            st.session_state.picture_taken = False
            st.session_state.upload_mode = None
            image_placeholder.empty()
        else:
            st.error("No image to save. Please take a picture first.")
