# Weathercast

![Weathercast icon](assets/PCLOUDY1.png)

A weather app built with Streamlit, Requests, and Open-Meteo. Search for a city to see current conditions and a seven-day forecast.

[Open the hosted app](https://weathercast-app.streamlit.app/)

Open-Meteo was chosen for its clear Python documentation and API access without a key.

## Setup

You need Python 3.10 or newer, pip, and an internet connection to retrieve weather data.

Clone the repository and open its folder:

```sh
git clone https://github.com/AdamOl135/Weathercast.git
cd Weathercast
```

On Windows, run these commands in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run src/main.py
```

On macOS or Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run src/main.py
```

Run the app from the repository root so it can find the icons in `assets/`. Streamlit opens the app in your browser, normally at [localhost:8501](http://localhost:8501). If it chooses another port, use the local URL printed in the terminal.

To stop the app, press `Ctrl+C` in that terminal. To start it again, run the Streamlit command for your operating system.

## How to use

1. The app starts with Berlin. Enter another city in **Search for City** and press `Enter`. Names with spaces, such as `New York`, work too.
2. Read the current-weather panels for temperature, feels-like temperature, today's high and low, humidity, wind speed, precipitation, sunrise, sunset, and UV index.
3. Scroll to **Weekly forecast** below the panels. It shows today and the next six days, with a condition icon, daily high and low, and total precipitation. The cards wrap on smaller screens.

Temperatures use Celsius, wind speed uses km/h, and precipitation uses millimeters. Forecast dates and sunrise and sunset times follow the searched city's timezone. Daily precipitation includes rain and the water equivalent of snow.

The search uses the first matching location returned by the geocoding service. Cities with the same name can therefore be ambiguous.

Successful results are cached for ten minutes to reduce repeated API calls. Reopening the same city during that time can show the cached forecast. The app requests new data when you search again after the cache expires.

If a city is not found, check the spelling and try again. If weather data is unavailable, check your connection and retry shortly. Restart the Streamlit process after changing `src/weather.py` if it still uses an older version of that module.

## Run the tests

The regression tests cover invalid searches, HTTP errors, forecast dates, UV timing, temperature precision, and icon availability. They use mocked API responses and do not require internet access.

On Windows:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

On macOS or Linux:

```sh
.venv/bin/python -m unittest discover -s tests -v
```

## Project structure

- `src/main.py` contains the Streamlit UI and weather-data cache.
- `src/weather.py` handles city lookup, forecast requests, and weather-code mapping.
- `assets/` contains the weather icons.
- `tests/` contains the regression tests.
- `requirements.txt` lists the pinned dependencies.






## Learning objectives

- Build from official Streamlit, Requests, and Open-Meteo documentation to practice reading specifications and solving problems without video tutorials.
- Keep application code inside `src/` to practice maintainable project layout.
- Separate the UI in `main.py` from API calls and weather-data processing in `weather.py`.


## Credits

- Weather icons: [WeatherNowIcons from Grabster](https://github.com/Grabstertv/WeatherNowIcons).
