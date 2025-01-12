import json
import requests
import cv2
import io
from PIL import Image
from openai import OpenAI
import os

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

def draw_bb(image_path, bounding_box):
    image = cv2.imread(image_path)

    x1 = int(bounding_box['x1'])
    y1 = int(bounding_box['y1'])
    x2 = int(bounding_box['x2'])
    y2 = int(bounding_box['y2'])

    color = (0, 255, 0)
    thickness = 2
    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

    output_path = 'uploaded_images/annotated_food.jpg'

    try:
        success = cv2.imwrite(output_path, image)
        if success:
            pass
        else:
            print("Failed to save the image")
    except Exception as e:
        print(f"An error occurred while saving the image: {str(e)}")

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

def delete_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

def main():
    image_path = "images/orange.jpg"

    try:
        image_object = Image.open(image_path)
        print("Image object created successfully.")

        result = call_api(image_object)

        food, food_bb, expiry = ask_ai(result)

        print("Here is a: " + food)
        draw_bb(image_path, food_bb)

        # delete_files("uploaded_images")
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
    except IOError:
        print(f"Error: Unable to open the image file '{image_path}'.")



main()
