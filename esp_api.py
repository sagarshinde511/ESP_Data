import streamlit as st
import requests
import time

# Streamlit App
st.title("Ultrasonic Sensor Distance Reader")

# API URL
api_url = "https://aeprojecthub.in/getdata.php?id=1&C=F1"

# Create a placeholder for dynamic content
placeholder = st.empty()

# Automatically refresh every second
while True:
    if api_url:  # Ensure the API URL is set
        try:
            # Make the GET request
            response = requests.get(api_url)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.text  # Get the data in string format

                # Parse the distance value from the data (assuming it's in a specific format)
                # Example format: "distance: XX cm"
                try:
                    # Extract the distance value (customize the parsing logic based on your API response)
                    if "distance:" in data:
                        distance_str = data.split("distance:")[1].strip().split(" ")[0]
                        distance = float(distance_str)
                    else:
                        distance = float(data.strip())  # Assume the data itself is the distance

                    # Update the placeholder with the distance value
                    with placeholder:
                        st.subheader(f"Distance: {distance} cm")
                except ValueError:
                    st.error("Failed to parse distance value from data.")

            else:
                st.error(f"Failed to fetch data. Status Code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    # Wait for 1 second before refreshing
    time.sleep(1)
