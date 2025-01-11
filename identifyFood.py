"""
All the data associated with identifying what the user is uploading.
"""

# Import statements
import cv2
import streamlit as st
import datetime

st.title('ShelfConcious')
st.write('Welcome! This page is made for you to take or upload pictures of your food. \n'
         'Please make sure to take a clear picture of a single food item you wish to log.'
         ' Press either of the two options below.')

# Initialize session state
if 'frame' not in st.session_state:
    st.session_state.frame = None
if 'picture_taken' not in st.session_state:
    st.session_state.picture_taken = False

left_spacer, col1, col2, right_spacer = st.columns([1, 1, 1, 1])

with col1:
    takePicture = st.button(label='Take a Picture')

with col2:
    st.button(label='Upload a Picture')

if takePicture:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        st.session_state.frame = frame
        st.session_state.picture_taken = True
        st.image(frame, channels="BGR")
    else:
        st.error("Failed to capture image. Please try again.")

left_spacer1, col3, right_spacer1 = st.columns([1, 1, 1])

if st.session_state.picture_taken:
    with col3:
        st.write("Please press \"Take a Picture\" again to retake. Press confirm picture to save.")
        confirmation = st.button(label='Confirm Picture')

    if confirmation:
        if st.session_state.frame is not None:
            cv2.imwrite('images/a.png', st.session_state.frame)
            st.success("Image saved successfully!")
            st.session_state.picture_taken = False  # Reset the state
        else:
            st.error("No image to save. Please take a picture first.")
