import openmeteo_requests
import requests
import time


#calling client
openmeteo = openmeteo_requests.Client()




def get_city(input_city:str):
	# GEOCODING
	# minimum 3 letters for search to work / location or postal code
	url_geocoding = "https://geocoding-api.open-meteo.com/v1/search"

	params_geocoding = {
		"name": input_city,
		"count": 1
	}

	# request to server
	# temporary solution for api request spam (10000 per day)
	time.sleep(1)
	responses_geocoding = requests.get(url_geocoding, params=params_geocoding, timeout=1)
	print("status code:", responses_geocoding.status_code)



	# response info from server(json)
	geocode_body = responses_geocoding.json()

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
		"daily": ["sunrise", "sunset", "temperature_2m_max", "temperature_2m_min"],
		"hourly": ["temperature_2m", "precipitation","uv_index"],
		"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "wind_speed_10m", "showers", "snowfall","cloud_cover"],
		"timezone": f"{timezone_geocode}",
		"minutely_15": "lightning_potential"
	}

	#request to api
	# temporary solution for api request spam (10000 per day)
	time.sleep(1)
	responses_forecast = openmeteo.weather_api(url_forecast, params = params_forecast)

	#if more locations need processing -> for loop

	response_forecast = responses_forecast[0]


	print("FROM HERE FORECAST STATEMENTS\n")
	#info from forecast api - time independent


	class WeatherData:
		#process non categorical
		latitude_forecast =response_forecast.Latitude()
		longitude_forecast = response_forecast.Longitude()
		elevation = response_forecast.Elevation()
		timezone = response_forecast.Timezone()
		timezone_difference_toGMT0 =response_forecast.UtcOffsetSeconds()
		print("forecast timezone",timezone)
		print("forecast timezone difference to gmt0",timezone_difference_toGMT0)
		print("forecast timezone difference to gmt0",type(timezone_difference_toGMT0),"\n")

		# Process minutely_15 data
		minutely_15 = response_forecast.Minutely15()
		minutely_15_lightning_potential = (minutely_15.Variables(0).ValuesAsNumpy())[0]

		#process current data (indexing dependent on params_forecast order)

		current = response_forecast.Current()
		current_time = current.Time()#unix ephttps://weathercast-app.streamlit.app/och (seconds since 1970)
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

		#process hourly data (indexing dependent on params_forecast order)
		hourly = response_forecast.Hourly()
		hourly_temperature = hourly.Variables(0).ValuesAsNumpy()#hours of 1 week
		hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()#hours of 1 week
		hourly_uv_index = hourly.Variables(2).ValuesAsNumpy()
		hourly_uv_index_1hour = int(hourly_uv_index[0])

		#process daily data (indexing dependent on params_forecast order)

		daily = response_forecast.Daily()
		daily_sunrise = int((daily.Variables(0).ValuesInt64AsNumpy())[0])#unix epoch (seconds since#
		# 1970), converted to int from array and reduced from 1 week to one day (index 0)
		daily_sunset = int((daily.Variables(1).ValuesInt64AsNumpy())[0])#unix epoch (seconds since#
		# 1970), converted to int from array and reduced from 1 week to one day (index 0)

		#converted to gmtime and added offset from weatherdata
		daily_sunrise_gmtime_adjusted = time.asctime(time.gmtime(daily_sunrise + timezone_difference_toGMT0))
		daily_sunset_gmtime_adjusted = time.asctime(time.gmtime(daily_sunset + timezone_difference_toGMT0))

		#convert with slicing first and then to int
		daily_temperature_2m_max = (daily.Variables(2).ValuesAsNumpy())[0]#1 week sliced to 1day
		daily_temperature_2m_max_int= int(daily_temperature_2m_max)#converted to int

		daily_temperature_2m_min = (daily.Variables(3).ValuesAsNumpy())[0]#1 week sliced to 1day
		daily_temperature_2m_min_int = int(daily_temperature_2m_min)#converted to int


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
			WeatherData.hourly_uv_index_1hour#16
	#todo : metric to imperial coversion if requested
	]


print("lightning:",(get_city("Bangkok")[16]))