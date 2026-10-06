import openmeteo_requests
import requests
import time
from datetime import datetime, timezone
import math


#calling client
openmeteo = openmeteo_requests.Client()




def get_city(input_city:str):
	input_city = input_city.strip()
	if len(input_city) < 2:
		raise ValueError("Enter a city name with at least two letters.")
	# GEOCODING
	# location or postal code
	url_geocoding = "https://geocoding-api.open-meteo.com/v1/search"

	params_geocoding = {
		"name": input_city,
		"count": 1
	}

	# request to server
	responses_geocoding = requests.get(url_geocoding, params=params_geocoding, timeout=10)
	responses_geocoding.raise_for_status()



	# response info from server(json)
	geocode_body = responses_geocoding.json()

	if not geocode_body.get("results"):
		raise ValueError("City not found. Check the spelling and try again.")
	# given location to server and converted to coordinates and timezone
	latitude_geocode = geocode_body["results"][0]["latitude"]
	longitude_geocode = geocode_body["results"][0]["longitude"]
	timezone_geocode = geocode_body["results"][0]["timezone"]




	# FORECAST

	url_forecast = "https://api.open-meteo.com/v1/forecast"

	#input params for request
	params_forecast = {
		"latitude": latitude_geocode,# params get passed from user input to geocoding to here
		"longitude": longitude_geocode,#
		"daily": ["sunrise", "sunset", "temperature_2m_max", "temperature_2m_min", "weather_code", "precipitation_sum"],
		"hourly": ["temperature_2m", "precipitation","uv_index"],
		"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "wind_speed_10m", "showers", "snowfall","cloud_cover", "weather_code"],
		"forecast_days": 7,
		"timezone": f"{timezone_geocode}",
		"minutely_15": "lightning_potential"
		#"models":"dwd_icon_seamless"
	}

	#request to api
	responses_forecast = openmeteo.weather_api(url_forecast, params = params_forecast, timeout=10)

	#if more locations need processing -> for loop

	response_forecast = responses_forecast[0]


	#info from forecast api - time independent


	class WeatherData:
		#process non categorical
		latitude_forecast =response_forecast.Latitude()
		longitude_forecast = response_forecast.Longitude()
		elevation = response_forecast.Elevation()
		timezone = response_forecast.Timezone()
		timezone_difference_toGMT0 =response_forecast.UtcOffsetSeconds()


		# Process minutely_15 data
		minutely_15 = response_forecast.Minutely15()
		minutely_15_lightning_potential = (minutely_15.Variables(0).ValuesAsNumpy())[0]

		#process current data (indexing dependent on params_forecast order)

		current = response_forecast.Current()
		current_time = current.Time()#unix epoch (seconds since 1970)
		current_temperature = round((current.Variables(0).Value()),1)
		current_relative_humidity = current.Variables(1).Value()
		current_apparent_temperature = current.Variables(2).Value()

		#icondata
		current_is_day = current.Variables(3).Value()
		current_precipitation = current.Variables(4).Value()
		current_rain = current.Variables(5).Value()
		current_wind_speed = current.Variables(6).Value()#in km/h
		current_showers = current.Variables(7).Value()
		current_snowfall = current.Variables(8).Value()
		current_cloud_cover = current.Variables(9).Value()
		current_weather_code = current.Variables(10).Value()

		#process hourly data (indexing dependent on params_forecast order)
		hourly = response_forecast.Hourly()
		hourly_temperature = hourly.Variables(0).ValuesAsNumpy()#hours of 1 week
		hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()#hours of 1 week
		hourly_uv_index = hourly.Variables(2).ValuesAsNumpy()
		hour_index = int((current_time - hourly.Time()) // hourly.Interval())
		hour_index = max(0, min(hour_index, len(hourly_uv_index) - 1))
		hourly_uv_index_1hour = round(float(hourly_uv_index[hour_index]), 1)

		#process daily data (indexing dependent on params_forecast order)

		daily = response_forecast.Daily()
		daily_sunrise = int((daily.Variables(0).ValuesInt64AsNumpy())[0])#unix epoch (seconds since#
		# 1970), converted to int from array and reduced from 1 week to one day (index 0)
		daily_sunset = int((daily.Variables(1).ValuesInt64AsNumpy())[0])#unix epoch (seconds since#
		# 1970), converted to int from array and reduced from 1 week to one day (index 0)

		#converted to gmtime and added offset from weatherdata
		daily_sunrise_gmtime_adjusted = time.asctime(time.gmtime(daily_sunrise + timezone_difference_toGMT0))
		daily_sunset_gmtime_adjusted = time.asctime(time.gmtime(daily_sunset + timezone_difference_toGMT0))

		# today's high and low temperatures
		daily_temperature_2m_max = (daily.Variables(2).ValuesAsNumpy())[0]#1 week sliced to 1day
		daily_temperature_2m_max_int= round(float(daily_temperature_2m_max), 1)

		daily_temperature_2m_min = (daily.Variables(3).ValuesAsNumpy())[0]#1 week sliced to 1day
		daily_temperature_2m_min_int = round(float(daily_temperature_2m_min), 1)

	# Keep the existing current-weather list; append the seven daily forecasts.
	weekly_forecast = []
	daily = WeatherData.daily
	for index, timestamp in enumerate(range(daily.Time(), daily.TimeEnd(), daily.Interval())):
		weekly_forecast.append({
			"date": datetime.fromtimestamp(timestamp + WeatherData.timezone_difference_toGMT0, timezone.utc).date(),
			"temperature_max": float(daily.Variables(2).ValuesAsNumpy()[index]),
			"temperature_min": float(daily.Variables(3).ValuesAsNumpy()[index]),
			"weather_code": float(daily.Variables(4).ValuesAsNumpy()[index]),
			"precipitation": float(daily.Variables(5).ValuesAsNumpy()[index]),
		})

	#needed values for app returned to main for usage
	return [WeatherData.current_temperature,#0
			WeatherData.current_apparent_temperature,#1
			WeatherData.daily_temperature_2m_max_int,#2
			WeatherData.daily_temperature_2m_min_int,#3
			WeatherData.current_relative_humidity,#4
			WeatherData.current_wind_speed,#5
			WeatherData.daily_sunrise_gmtime_adjusted,#6
			WeatherData.daily_sunset_gmtime_adjusted,#7
			WeatherData.current_is_day,#8
			WeatherData.current_precipitation,#9
			WeatherData.current_rain,#10
			WeatherData.current_wind_speed,#11
			WeatherData.current_showers,#12
			WeatherData.current_snowfall,#13
			WeatherData.current_cloud_cover,#14
			WeatherData.minutely_15_lightning_potential,#15
			WeatherData.hourly_uv_index_1hour,#16
			geocode_body,#17
			response_forecast,#18
			WeatherData.current,#19
			weekly_forecast,#20
			WeatherData.current_weather_code,#21
	#todo : metric to imperial coversion if requested
	]


def get_weather_icon(weather_code, is_day=1):
	"""Return an existing icon and description for an Open-Meteo weather code."""
	variant = 1 if is_day else 0
	if not math.isfinite(weather_code):
		return "assets/MCLOUDY.png", "Unavailable"
	code = int(weather_code)
	if code in (0, 1):
		return f"assets/CLEAR{variant}.png", "Clear" if code == 0 else "Mainly clear"
	if code == 2:
		return f"assets/PCLOUDY{variant}.png", "Partly cloudy"
	if code == 3:
		return "assets/MCLOUDY.png", "Overcast"
	if code in (45, 48):
		return "assets/MCLOUDY.png", "Fog"
	if code in (51, 53, 55):
		return f"assets/SHOWER{variant}.png", "Drizzle"
	if code in (56, 57, 66, 67):
		return f"assets/SLEET{variant}.png", "Freezing rain"
	if code in (61, 63, 65, 80, 81, 82):
		return f"assets/SHOWER{variant}.png", "Rain"
	if code in (71, 73, 75, 77, 85, 86):
		return f"assets/LSNOW{variant}.png", "Snow"
	if code in (95, 96, 97, 99):
		return f"assets/TSTORM{variant}.png", "Thunderstorm"
	return "assets/MCLOUDY.png", "Unavailable"
