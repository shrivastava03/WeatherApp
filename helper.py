from geopy.geocoders import Nominatim
import streamlit as st
import requests

def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="weather-app")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None


def validate_coordinates(coord_string):
    try:
        lat_str, lon_str = coord_string.split(",")
        lat, lon = float(lat_str.strip()), float(lon_str.strip())

        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon
        else:
            return None, None
    except:
        return None, None


def get_weather(lat, lon, mode):
    api_key = st.secrets["weather_api"] # Add the api key instad of st.secrets["weather_api"]
    if mode == "current":
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    elif mode == "forecast":
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    else:
        return None
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def deg_to_compass(num):
    val = int((num / 22.5) + 0.5)
    directions = ["North", "North-Northeast", "Northeast", "East-Northeast",
                  "East", "East-Southeast", "Southeast", "South-Southeast",
                  "South", "South-Southwest", "Southwest", "West-Southwest",
                  "West", "West-Northwest", "Northwest", "North-Northwest"]
    return directions[val % 16]