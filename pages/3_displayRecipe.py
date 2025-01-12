import streamlit as st
import os
from openai import OpenAI


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

if st.button(label='Return to Home'):
    st.switch_page("pages/1_displayoptions.py")

def ask_ai_for_recipes(food_list):
    # Combine the list of foods into a single string
    food_string = ", ".join(food_list)

    API_KEY = "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"

    client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

    # Create the prompt for recipe generation
    prompt = (
        f"I have the following ingredients: {food_string}. "
        "Please provide a list of recipes I can make with these ingredients. "
        "Include as many recipes as possible and provide them in this format: "
        "'Recipe 1 Name: Ingredients that it uses from the list given + Recipe 2 Name: Ingredients that it uses from the list given + Recipe 3 Name: Ingredients that it uses from the list given'. The ingredients should match my list."
        "THE LIST SHOULD BE YOUR ENTIRE RESPONSE, NOTHING ELSE"
    )

    # Set up the chat messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI chef and will provide recipes based on the user's ingredients. "
                "Respond exactly as requested, using the specified format."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    # Call the API
    response = client.chat.completions.create(
        model="llama-3.1-sonar-large-128k-online",
        messages=messages,
    )

    # Extract the response
    response_text = response.choices[0].message.content
    return response_text.split(" + ")
def save_list_as_md(my_list, filename="recipes.md", directory= 'pages'):
    md_content = ""
    for item in my_list:
        md_content += f" {item}\n-"
    file_path = os.path.join(directory, filename)

    with open(file_path, "w") as f:
        f.write(md_content)

# Example list of foods
food_list = ["chicken", "garlic", "onion", "tomato"]

# Get recipes from the AI
recipes = ask_ai_for_recipes(food_list)
save_list_as_md(recipes)

st.write("Recipes")
st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)

with open('pages/recipes.md', 'r') as file:
    lines = file.readlines()
lines = lines[:-1]
content = ''.join(lines)
st.write(content)
