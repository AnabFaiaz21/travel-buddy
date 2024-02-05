from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import requests

from geopy.geocoders import Nominatim
import os
import webbrowser

app = FastAPI()

class City(BaseModel):
    name: str

class Attraction(BaseModel):
    name: str
    latitude: float
    longitude: float
    category: str

def get_city_coordinates(city_name):
    geolocator = Nominatim(user_agent="city_locator")
    location = geolocator.geocode(city_name)

    if location:
        return [location.latitude, location.longitude]
    else:
        print(f"Could not find coordinates for {city_name}")

def fetch_nearby_attractions(latitude, longitude, categories):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": categories,
        "format": "json",
        "limit": 20,
        "bounded": 1,
        "viewbox": f"{longitude - 0.2},{latitude - 0.2},{longitude + 0.2},{latitude + 0.2}",
        "addressdetails": 1,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_marker_color(category):
    colors = {"beach": "orange", "park": "green", "restaurant": "pink", "hospital": "red"}
    return colors.get(category, "blue")

def get_marker_icon(category):
    icons = {"beach": "umbrella-beach", "park": "tree", "restaurant": "utensils", "hospital": "hospital"}
    return icons.get(category, "home")

@app.post("/get_attractions/")
async def get_attractions(city_name: str = Query(..., description="Name of the city for which to fetch attractions")):
    city = City(name=city_name)  # Validate city_name using the model

    coordinates = get_city_coordinates(city_name)
    if not coordinates:
        raise HTTPException(status_code=404, detail="City not found")

    attractions = []
    for category in ["beach", "park", "restaurant", "hospital"]:
        attractions_data = fetch_nearby_attractions(coordinates[0], coordinates[1], [category])
        for attraction_data in attractions_data:
            attractions.append(Attraction(name=attraction_data["display_name"], latitude=attraction_data["lat"], longitude=attraction_data["lon"], category=category))

    map_obj = folium.Map(location=coordinates, zoom_start=12)
    folium.Marker(
        location=coordinates,
        tooltip=f"{city.name}",
        icon=folium.Icon(color="blue", icon="home")  # Custom icon for listings
    ).add_to(map_obj)

    for attraction in attractions:
        icon = folium.Icon(color=get_marker_color(attraction.category), icon=get_marker_icon(attraction.category), prefix='fa')
        folium.Marker(location=[attraction.latitude, attraction.longitude], icon=icon, tooltip=attraction.name).add_to(map_obj)

    map_file = "map.html"
    map_obj.save(map_file)
    #webbrowser.open(f"file://{os.path.abspath(map_file)}")
    #return {"map_url": f"file://{os.path.abspath(map_file)}"}