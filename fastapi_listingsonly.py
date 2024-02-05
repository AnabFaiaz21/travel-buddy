import pandas as pd
import folium
import webbrowser
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/listings_map")
async def create_listings_map(city_name: str = Query(..., description="Enter the city name to generate the map for")):
    # Load data
    listings_data = pd.read_csv("Austrailia_listings.csv")

    # Filter listings
    filtered_listings = listings_data[listings_data["city"].str.lower() == city_name.lower()]

    # Create map centered on city
    latitude = filtered_listings["latitude"].mean()
    longitude = filtered_listings["longitude"].mean()
    map_obj = folium.Map(location=[latitude, longitude], zoom_start=12)

    # Add markers for each listing
    for index, listing in filtered_listings.iterrows():
        listing_location = [listing["latitude"], listing["longitude"]]
        folium.Marker(location=listing_location, tooltip=f"{listing['name']} ({listing['city']})").add_to(map_obj)

    # Save the map as an HTML file
    map_obj.save("listings_map.html")

    # Return the HTML content as the API response
    with open("listings_map.html", "r") as f:
        html_content = f.read()
    return html_content
webbrowser.open("listings_map.html")