import streamlit as st
from fastapi import FastAPI
from pyngrok import ngrok
from pathlib import Path

# Import your FastAPI app here
from try2 import app  # Assuming your FastAPI app is in a file named `try.py`

# Start the FastAPI app in the background
fast_api_server = FastAPI()
fast_api_server.mount("/get_attractions", app)

@st.cache(allow_output_mutation=True)
def start_ngrok():
    url = ngrok.connect(8000).public_url
    return url

ngrok_url = start_ngrok()

def get_map_url(city_name):
    response = requests.post(f"{ngrok_url}/get_attractions/", json={"city_name": city_name})
    return response.json()["map_url"]

st.title("Explore City Attractions")

city_name = st.text_input("Enter a city name:")

if city_name:
    map_url = get_map_url(city_name)
    st.markdown(f"**Generated Map:**")
    st.components.iframe(map_url, width=800, height=600)
