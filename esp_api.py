import streamlit as st
import requests

# Streamlit App
st.title("Check Recived Data From Hardware")

# Input for API URL
api_url = "https://aeprojecthub.in/getdata.php?id=1&C=F1"

# Button to fetch data
if st.button("Fetch Data"):
    try:
        # Make the GET request
        response = requests.get(api_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Display the data in a formatted way
            st.success("Data fetched successfully!")
            st.json(data)  # Display JSON data in a formatted manner
        else:
            st.error(f"Failed to fetch data. Status Code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
