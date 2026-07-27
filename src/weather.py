import openmeteo_requests

#calling client
openmeteo = openmeteo_requests.Client()

city_search_name = ""

urlforecast = "https://api.open-meteo.com/v1/forecast"

# minimum 3 letters for search to work / location or postal code
geocodingurl = f"https://geocoding-api.open-meteo.com/v1/search?name={city_search_name}&count=5&language=en&format=json"


lattitude = 49.5489
longitude = 8.667

params = {
	"latitude": lattitude,
	"longitude": longitude,
	"daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration"],
	"hourly": ["temperature_2m", "precipitation", "cloud_cover", "visibility", "is_day", "lightning_potential"],
	"models": "dwd_icon_seamless",
	"current": ["temperature_2m", "relative_humidity_2m", "precipitation", "rain", "showers", "snowfall", "wind_speed_10m", "apparent_temperature"],
	"timezone": "Europe/Berlin",
}
responses = openmeteo.weather_api(urlforecast, params = params)

response = responses[0]
#general info - time independent