# weather.py
import requests
from ss import key2  # Import your API key

def get_weather():
    api_address = 'http://api.openweathermap.org/data/2.5/weather?q=Vietnam&appid=' + key2
    json_data = requests.get(api_address).json()
    
    temperature = round(json_data["main"]["temp"] - 273, 1)
    description = json_data["weather"][0]["description"]
    if "main" in json_data and "temp" in json_data["main"] and "weather" in json_data and len(json_data["weather"]) > 0:
        temperature = round(json_data["main"]["temp"] - 273, 1)
        description = json_data["weather"][0]["description"]
        return temperature, description
    else:
        print("Failed to fetch weather data.")
        return None