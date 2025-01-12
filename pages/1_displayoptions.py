
import streamlit as st
import pandas as pd
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

# Display the current date
file_path = 'items.csv'

# Load the CSV file
df = pd.read_csv(file_path)

# Convert the 'Expiry Date' column to datetime format (if it's not already)
df['Expiry Date'] = pd.to_datetime(df['Expiry Date'], errors='coerce')
# the .sort_values method returns a new dataframe, so make sure to
# assign this to a new variable.
sorted_df = df.sort_values(by=["Expiry Date"], ascending=True)
sorted_df['Expiry Date'] = sorted_df['Expiry Date'].dt.date

sorted_df.to_csv('items.csv', index=False)

# header for this page
st.title("Item Tracker")
st.write("Current Date:", datetime.now().strftime('%Y-%m-%d'))

# Get the current date as a datetime object (instead of a date object)
current_date = pd.Timestamp(datetime.now()).date()

# Calculate the date one week from now, one month from now
one_week_from_now = current_date + timedelta(days=7)
one_month_from_now = current_date + timedelta(weeks=4)

# store data in Alerts for expire in a week, and expire in a month

alerts_df = sorted_df[(sorted_df['Expiry Date'] >= current_date) & (sorted_df['Expiry Date'] <= one_week_from_now)]
alerts2_df = sorted_df[(sorted_df['Expiry Date'] >= current_date) & (sorted_df['Expiry Date'] <= one_month_from_now)
                       & (sorted_df['Expiry Date'] > one_week_from_now)]
expired_df = sorted_df[(sorted_df['Expiry Date'] <= current_date)]

# # CSS code for ALERTS header
st.markdown(
    """
    <style>
    .burgundy-header {
        color: #800020;
        font-size: 36px;
        font-weight: bold;
        text-align: left;
        margin-bottom: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the ALERTS header
st.markdown('<div class="burgundy-header">Alerts</div>', unsafe_allow_html=True)

# CSS code for Expires in _ header
st.markdown(
    """
    <style>
    .burgundy-header2 {
        color: #800020;
        font-size: 26px;
        font-weight: bold;
        text-align: left;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom CSS for the box
st.markdown(
    """
    <style>
    .custom-box {
        background-color: #f8f9fa;  /* Light background color */
        border: 2px solid #800020;  /* Burgundy border color */
        border-radius: 10px;  /* Rounded corners */
        padding: 20px;  /* Padding inside the box */
        font-size: 25px;  /* Font size */
        font-weight: bold;  /* Font weight */
        color: #800020;  /* Burgundy text color */
        margin-bottom: 20px;  /* Space below the box */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the box with text inside it
if not expired_df.empty:
    for index, row in expired_df.iterrows():
        item = row['Item']
        # Insert the expired item text inside the box
        st.markdown(f'<div class="custom-box">{item} **EXPIRED**</div>', unsafe_allow_html=True)
else:
    st.write("No items are expired!")



# Displays Expires This Week items
st.markdown('<div class="burgundy-header2">‼️Expires This Week</div>', unsafe_allow_html=True)
if not alerts_df.empty:
    for index, row in alerts_df.iterrows():
        item = row['Item']
        expiry_date = row['Expiry Date']
        days_left = (expiry_date - current_date).days
        st.write(f"**{item}** expires in **{days_left} day(s)**")
else:
    st.write("No items are expiring within the next week!")


# Display Expires This Month items
st.markdown('<div class="burgundy-header2">❗️Expires This Month</div>', unsafe_allow_html=True)

if not alerts2_df.empty:
    for index, row in alerts2_df.iterrows():
        item = row['Item']
        expiry_date = row['Expiry Date']
        days_left = (expiry_date - current_date).days
        st.write(f"**{item}** expires in **{days_left} day(s)**")
else:
    st.write("No items are expiring after this week.")

st.divider()

col1, col2 = st.columns(2)
updated_df = df.copy()


# Display items in the first column and expiry dates in the second WITH CHECKBOXES try1
# **BUG: must check box twice in order for it to be deleted :(
with col1:
    st.subheader("Item")
    for index, row in sorted_df.iterrows():
        checkbox = st.checkbox(row['Item'], key=f"item_{index}")
        if checkbox:
            st.success("Item removed from list")
            st.balloons()
            updated_df = updated_df.drop(index)

with col2:
    st.subheader("Expiry Date")
    for expiry_date in sorted_df['Expiry Date']:
        st.write(expiry_date)

# Saves the Updated DataFrame to the CSV
if not updated_df.equals(sorted_df):
    updated_df.to_csv(file_path, index=False)

# Add Item button
col = st.columns(2)
with col[0]:
    add = st.button("Add Item", use_container_width=True)  # Full-width button that goes to lily's page!
with col[1]:
    recipe = st.button("Find Recipes", use_container_width=True)
if add:
    st.switch_page("pages/2_identifyFood.py")
if recipe:
    st.switch_page("pages/3_displayRecipe.py")
