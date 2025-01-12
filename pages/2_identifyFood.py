"""
All the data associated with identifying what the user is uploading.
"""

# Import statements
import cv2
import streamlit as st
import numpy as np
from _datetime import datetime
import json
import requests
import cv2
import io
from PIL import Image, ImageEnhance
from openai import OpenAI
import os
import csv
from datetime import datetime, timedelta


def set_background_from_url(url):
    st.markdown(
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

def delete_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

def call_api(img, max_size=(2000, 2000)):
    api_url = 'https://api.api-ninjas.com/v1/objectdetection'

    if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
        img.thumbnail(max_size, Image.LANCZOS)

    # Convert the image to bytes
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_bytes = buffer.getvalue()

    files = {'image': ('image.jpg', img_bytes, 'image/jpeg')}

    r = requests.post(api_url, headers={'X-Api-Key': 'cHp4ZabWUnYryfx7A5ErwQ==IjIskOoZyBoVQWpt'}, files=files)
    r_string = str(r.json()).replace("'", '"')

    return json.loads(r_string)

def draw_bb(pil_image, bounding_box):
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    x1 = int(bounding_box['x1'])
    y1 = int(bounding_box['y1'])
    x2 = int(bounding_box['x2'])
    y2 = int(bounding_box['y2'])

    color = (0, 255, 0)
    thickness = 2
    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

    # Convert the image back to RGB color space
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a PIL Image from the numpy array
    return Image.fromarray(rgb_image)

def ask_ai(api_input):
    current_food = api_input[0]["label"]
    current_bb = api_input[0]["bounding_box"]

    API_KEY = "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"

    client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {
            "role": "user",
            "content": (
                    "Is " + current_food + " an edbile food that humans regulary consume? Respond exactly in the following format: ['y/n', expiration date in days]. "
                                   "For example, if the food is a pear, your response would be ['y',5] but if the input "
                                   "food was 'desk', your response should be ['n',0]. Lastly, if the food has a range, "
                                   "like 10-14, give the lower value. THE LIST SHOULD BE YOUR ENTIRE RESPONSE, NOTHING ELSE, "
                                           "EVEN IF THINGS VARY OR NOT. EITHER ['y',_] or ['n',0]"
            ),
        },
    ]

    response = client.chat.completions.create(
        model="llama-3.1-sonar-large-128k-online",
        messages=messages,
    )

    response = response.choices[0].message.content
    expiry = response[6]

    return current_food, current_bb, expiry

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
        image_placeholder.empty()
        st.session_state.picture_taken = False

with col2:
    if st.button(label='Upload a Picture'):
        st.session_state.upload_mode = 'upload'
        upload_placeholder.empty()
        st.session_state.picture_taken = False

# Handle camera capture
if st.session_state.upload_mode == 'camera':
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        st.session_state.frame = frame
        st.session_state.picture_taken = True

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_rgb = cv2.convertScaleAbs(frame_rgb, alpha=1.5, beta=20)

        pil_image = Image.fromarray(frame_rgb)

        result = call_api(pil_image)
        food, food_bb, expiry = ask_ai(result)
        bb_image = draw_bb(pil_image, food_bb)

        image_placeholder.image(bb_image, channels="RGB")

        with open('items.csv', mode='a', newline='') as file:
            writer = csv.writer(file)

            current_date = datetime.now()
            expiry_date = current_date + timedelta(days=float(expiry))
            expiry_date_str = expiry_date.strftime('%Y-%m-%d')

            writer.writerow([food, expiry_date_str])

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

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)

            result = call_api(pil_image)
            food, food_bb, expiry = ask_ai(result)

            bb_image = draw_bb(pil_image, food_bb)

            image_placeholder.image(bb_image, channels="BGR")

            with open('items.csv', mode='a', newline='') as file:
                writer = csv.writer(file)

                current_date = datetime.now()
                expiry_date = current_date + timedelta(days=float(expiry))
                expiry_date_str = expiry_date.strftime('%Y-%m-%d')

                writer.writerow([food, expiry_date_str])

        else:
            st.error("Failed to process image. Please try again.")

# Confirmation button
if st.session_state.picture_taken:
    confirmation = confirm_placeholder.button(label='Confirm Picture', use_container_width=True)
    if confirmation:
        confirm_placeholder.empty()
        upload_placeholder.empty()
        if st.session_state.frame is not None:
            curr_datetime = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            cv2.imwrite('uploaded_images/' + curr_datetime + '.png', st.session_state.frame)
            st.success("Image saved successfully!")
            st.session_state.picture_taken = False
            st.session_state.upload_mode = None
            image_placeholder.empty()
        else:
            st.error("No image to save. Please take a picture first.")
