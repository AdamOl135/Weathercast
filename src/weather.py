import openmeteo_requests
import requests


#calling client
openmeteo = openmeteo_requests.Client()


#GEOCODING

#user input for city
city_search_name = "mannheim"

# minimum 3 letters for search to work / location or postal code
url_geocoding = "https://geocoding-api.open-meteo.com/v1/search"


params_geocoding = {
	"name":city_search_name,
	"count":1
}

#request to server
responses_geocoding = requests.get(url_geocoding,params = params_geocoding)

#response info from server(json)
geocode_body = responses_geocoding.json()

# given location to server and converted to coordinates
latitude = geocode_body["results"][0]["latitude"]
longitude = geocode_body["results"][0]["longitude"]





# FORECAST

url_forecast = "https://api.open-meteo.com/v1/forecast"

params_forecast = {
	"latitude": latitude,# params get passed from user input to geocoding to here
	"longitude": longitude,#
	"daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration"],
	"hourly": ["temperature_2m", "precipitation", "cloud_cover", "visibility", "is_day", "lightning_potential"],
	"models": "dwd_icon_seamless",
	"current": ["temperature_2m", "relative_humidity_2m", "precipitation", "rain", "showers", "snowfall", "wind_speed_10m", "apparent_temperature"],
	"timezone": "Europe/Berlin",
}


responses_forecast = openmeteo.weather_api(url_forecast, params = params_forecast)

#if more locations need processing -> for loop

response_forecast = responses_forecast[0]

#general info - time independent


print(f"Coordinates forecast:{response_forecast.Latitude()},")