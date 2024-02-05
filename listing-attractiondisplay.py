import pandas as pd
import folium
import requests

import webbrowser

listings_data = pd.read_csv("Austrailia_listings.csv")
city_name = input("Enter the city name: ")

# Filter listings
filtered_listings = listings_data[listings_data["suburb"].str.lower() == city_name.lower()]

# Create map centered on city
latitude = filtered_listings["latitude"].mean()
longitude = filtered_listings["longitude"].mean()
map_obj = folium.Map(location=[latitude, longitude], zoom_start=12)


for index, listing in filtered_listings.iterrows():
    listing_lat = listing["latitude"]
    listing_lon = listing["longitude"]

    # Add listing marker
    folium.Marker(
        location=[listing_lat, listing_lon],
        tooltip=f"{listing['name']} {listing['city']})",
        icon=folium.Icon(color="blue", icon="home"),  # Custom icon for listings
    ).add_to(map_obj)


# Add markers for nearby attractions
def fetch_nearby_attractions(latitude, longitude, categories):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": categories,
        "format": "json",
        "limit": 10,
        "bounded": 1,
        "viewbox": f"{longitude - 0.2},{latitude - 0.2},{longitude + 0.2},{latitude + 0.2}",
        "addressdetails": 1,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

beaches = fetch_nearby_attractions(latitude, longitude, ["beach"])
for beachh in beaches:
    lat = beachh["lat"]
    lng = beachh["lon"]
    name = beachh["display_name"]
    folium.Marker(location=[lat, lng], icon=folium.Icon(color="orange", icon="umbrella-beach",prefix='fa'), tooltip=name).add_to(
        map_obj
    )

parks = fetch_nearby_attractions(latitude, longitude, ["park"])
for parkk in parks:
    lat = parkk["lat"]
    lng = parkk["lon"]
    name = parkk["display_name"]
    folium.Marker(location=[lat, lng], icon=folium.Icon(color="green", icon="tree", prefix="fa"), tooltip=name).add_to(
        map_obj
    )

restaurants = fetch_nearby_attractions(latitude, longitude, ["restaurant"])
for restaurantss in restaurants:
    lat = restaurantss["lat"]
    lng = restaurantss["lon"]
    name = restaurantss["display_name"]
    folium.Marker(location=[lat, lng], icon=folium.Icon(color="pink", icon="utensils",prefix='fa'), tooltip=name).add_to(
        map_obj
    )

hospitals = fetch_nearby_attractions(latitude, longitude, ["hospital"])
for hospitalss in restaurants:
    lat = hospitalss["lat"]
    lng = hospitalss["lon"]
    name = hospitalss["display_name"]
    folium.Marker(location=[lat, lng], icon=folium.Icon(color="red", icon="hospital",prefix='fa'), tooltip=name).add_to(
        map_obj
    )
# Save and display the map
map_obj.save("listings_map_with_attractions.html")
print(
    f"Map of listings and nearby attractions in {city_name} saved as listings_map_with_attractions.html"
)

webbrowser.open("listings_map_with_attractions.html")
