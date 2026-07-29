import openmeteo_requests
import requests
import time



#calling client
openmeteo = openmeteo_requests.Client()


#GEOCODING

#user input for city
city_search_name = "bucharest"

# minimum 3 letters for search to work / location or postal code
url_geocoding = "https://geocoding-api.open-meteo.com/v1/search"


params_geocoding = {
	"name":city_search_name,
	"count":1
}

#request to server
responses_geocoding = requests.get(url_geocoding,params = params_geocoding)

#temporary solution for api request spam (10000 per day)
time.sleep(0)

#response info from server(json)
geocode_body = responses_geocoding.json()

# given location to server and converted to coordinates and timezone
latitude_geocode = geocode_body["results"][0]["latitude"]
longitude_geocode = geocode_body["results"][0]["longitude"]
timezone_geocode = geocode_body["results"][0]["timezone"]


print("latitude geocode",latitude_geocode)
print("longitude_geocode",longitude_geocode)
print("timezone",timezone_geocode,"\n")


# FORECAST

url_forecast = "https://api.open-meteo.com/v1/forecast"

#input params for request
params_forecast = {
	"latitude": latitude_geocode,# params get passed from user input to geocoding to here
	"longitude": longitude_geocode,#
	"daily": ["sunrise", "sunset", "temperature_2m_max", "temperature_2m_min"],
	"hourly": ["temperature_2m", "precipitation","uv_index"],
	"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "wind_speed_10m", "showers", "snowfall"],
	"timezone": f"{timezone_geocode}",
}

#request to api
responses_forecast = openmeteo.weather_api(url_forecast, params = params_forecast)

#if more locations need processing -> for loop

response_forecast = responses_forecast[0]


print("FROM HERE FORECAST STATEMENTS\n")
#info from forecast api - time independent


class weather_data:
	#process non categorical
	latitude_forecast =response_forecast.Latitude()
	longitude_forecast = response_forecast.Longitude()
	elevation = response_forecast.Elevation()
	timezone = response_forecast.Timezone()
	timezone_difference_toGMT0 =response_forecast.UtcOffsetSeconds()
	print("forecast timezone",timezone)
	print("forecast timezone difference to gmt0",timezone_difference_toGMT0)

	#process current data (indexing dependent on params_forecast order)

	current = response_forecast.Current()
	current_time = current.Time()#unix epoch (seconds since 1970)
	current_temperature = current.Variables(0).Value()
	current_relative_humidity = current.Variables(1).Value()
	current_apparent_temperature = current.Variables(2).Value()
	current_is_day = current.Variables(3).Value()
	current_precipitation = current.Variables(4).Value()
	current_rain = current.Variables(5).Value()
	current_wind_speed = current.Variables(6).Value()#in km/h
	current_showers = current.Variables(7).Value()
	current_snowfall = current.Variables(8).Value()

	#process hourly data (indexing dependent on params_forecast order)
	hourly = response_forecast.Hourly()
	hourly_temperature = hourly.Variables(0).ValuesAsNumpy()#hours of 1 week
	hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()#hours of 1 week
	hourly_uv_index = hourly.Variables(2).ValuesAsNumpy()


	#process daily data (indexing dependent on params_forecast order)
	daily = response_forecast.Daily()
	daily_sunrise = daily.Variables(0).ValuesInt64AsNumpy()#unix epoch (seconds since 1970)
	daily_sunset = daily.Variables(1).ValuesInt64AsNumpy()#unix epoch (seconds since 1970)

	daily_temperature_2m_max = daily.Variables(2).ValuesAsNumpy()  # 1 week
	daily_temperature_2m_min = daily.Variables(3).ValuesAsNumpy()  # 1 week

	#converted from array with 1 week info to int with 1 day info
	daily_sunrise_converted_oneday2 = int(daily_sunrise[0])

	# converted sunrise/sunset from unix to date and one day
	#todo, convert gm time with given timezone into offset and add to sunrise/set, offset already in forecast variables
	daily_sunset_converted_timeadjusted_3 = time.asctime(time.gmtime(daily_sunrise_converted_oneday2,),)




print("sunrise unprocessed",weather_data.daily_sunrise[0],"sunset unprocessed",weather_data.daily_sunset[0])
print("converted with gmtime",weather_data.daily_sunset_converted_timeadjusted_3)





