import streamlit as st
import pandas as pd

# Create sample data with latitude and longitude
data = pd.DataFrame({
    'lat': [17.2987556,17.29085],
    'lon': [74.1900642,74.1842447]
})

# Display a map
st.map(data)
