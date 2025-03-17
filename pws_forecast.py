### The model relies on Event Stream Processing (ESP)
import requests
import json
import datetime
import time
from collections import deque
from ambient_api.ambientapi import AmbientAPI



# Fetch data from the Ambient Weather API
def fetch_weather_data(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200: # Response success code check
            data = response.json()
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

AMBIENT_ENDPOINT = https://rt.ambientweather.net/v1
AMBIENT_API_KEY = "" # Insert API key here
AMBIENT_APPLICATION_KEY = "" # Insert application key here
api = AmbientAPI()

weather_data = fetch_weather_data(endpoint=AMBIENT_ENDPOINT, api_key=AMBIENT_API_KEY, application_key=AMBIENT_APPLICATION_KEY)
if weather_data:
    print(json.dumps(weather_data, indent=2))


def process_weather_data(data):
    pressure = data['pressure']
    wind_direction = data['wind_direction']
    season = determine_season()
    pressure_trend = calculate_pressure_trend(pressure)
    daily_rain = data['daily_rain']
    sunlight = data['lux']
    # Other parameters can be added as needed


    return pressure, wind_direction, pressure_trend, season


def determine_season():
    month = datetime.datetime.now().month

    if 3 <= month <= 5:
        return "spring"
    elif 6 <= month <= 8:
        return "summer"
    elif 9 <= month <= 11:
        return "autumn"
    else:
        return "winter"
    

pressure_history = deque(maxlen=5) # Initializes a deque to store the last "maxlen" pressure readings

def calculate_pressure_trend(current_pressure):
    pressure_history.append(current_pressure)

    if len(pressure_history) < 2:
        return "steady" # This is a compromise, as len < 2 is an insufficient data size
    
    if pressure_history[-1] > pressure_history[-2]:
        return "rising"
    elif pressure_history[-1] < pressure_history[-2]:
        return "falling"
    else:
        return "steady"
    

rain_history = deque(maxlen=4) # Slots allocated for rain history memory

def calculate_rain_trend(current_rain):
    rain_history.append(current_rain)

    if len(rain_history) < 2:
        return "steady"
    
    if rain_history[-1] > rain_history[-2]:
        return "increasing rainfall"
    elif rain_history[-1] < rain_history[-2]:
        return "decreasing rainfall"
    else:
        return "steady rainfall"


def zambretti_demirkol_forecast(pressure, trend, wind_direction, season):
    if trend == "rising":
        if pressure > 1020:
            return "Fine weather"
        elif pressure > 1010:
            return "Becoming fine"
        else:
            return "Changeable, becoming fine"
        
    elif trend == "steady":
        if pressure > 1020:
            return "Fair"
        elif pressure > 1010:
            return "Cloudy, possible showers"
        else:
            return "Unsettled"
        
    elif trend == "falling":
        if pressure > 1020:
            return "Showers"
        elif pressure > 1010:
            return "Rain"
        else:
            return "Stormy weather"
    
    if wind_direction == "N":
        return "Cold and unsettled"
    
    elif wind_direction == "S":
        return "Warm and rainy"
    
    if season == "winter" and trend == "falling":
        return "Snow possible"
    
    return "No prediction available"


while True:
    weather_data = fetch_weather_data(AMBIENT_ENDPOINT)

    if weather_data:
        pressure, wind_direction, pressure_trend, season = process_weather_data(weather_data)
        forecast = zambretti_demirkol_forecast(pressure, pressure_trend, wind_direction, season)

        print(f"Current forecast: {forecast}")

        time.sleep(600) # Fetches data every "sleep" seconds