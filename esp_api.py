import streamlit as st
import requests
import time

# Streamlit App
st.title("ESP Data Reader")

# API URL
api_url = "https://aeprojecthub.in/getdata.php?id=1&C=F1"

# Automatically refresh every second
while True:
    if api_url:  # Ensure the API URL is set
        try:
            # Make the GET request
            response = requests.get(api_url)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.text  # Get the data in string format
                st.text(data)  # Display the data as plain text
            else:
                st.error(f"Failed to fetch data. Status Code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    # Wait for 1 second before refreshing
    time.sleep(1)
    #st.experimental_rerun()  # Rerun the app
