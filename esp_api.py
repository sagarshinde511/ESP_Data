import streamlit as st
import requests

# Streamlit App
st.title("ESP Data Reader")
while(1):
# Input for API URL
    api_url = "https://aeprojecthub.in/getdata.php?id=1&C=F1";
    
    if api_url:  # Check if the user entered an API URL
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
