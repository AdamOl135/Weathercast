import streamlit as st
import requests
import math
from openmeteo_requests import OpenMeteoRequestsError
from weather import get_city, get_weather_icon


@st.cache_data(ttl=600, max_entries=128, show_spinner=False)
def load_weather(city):
    return get_city(city)


def format_forecast_value(value, unit):
    return f"{value:.1f}{unit}" if math.isfinite(value) else "Unavailable"

st.set_page_config(
    page_title="Weathercast",
    page_icon="assets/PCLOUDY1.png",
    layout = "wide",
    menu_items={
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

#top row with logo, app name and search function
with st.container(horizontal=True, horizontal_alignment = "distribute",width="stretch"):

    #logo & Title
    logo = st.image(image="assets/PCLOUDY1.png",width = 45,output_format="PNG")
    name = st.header(body="Weathercast",text_alignment="left")

    #spacing between elements
    st.space("stretch")


    #search button for city with max input as safety precaution
    search = st.text_input(
    label = "placeholder",
    label_visibility="collapsed",
    max_chars=100,
    placeholder = "Search for City",
    persist_state= "page",
    key="CityInput",
    disabled=False,
    value="Berlin",
    icon=":material/search:",
    width=300)

    try:
        all_weather_info = load_weather(search.strip())
    except ValueError as error:
        st.warning(str(error))
        st.stop()
    except (requests.RequestException, OpenMeteoRequestsError):
        st.error("Weather data is unavailable. Please try again shortly.")
        st.stop()


    weather_icon, _ = get_weather_icon(all_weather_info[21], all_weather_info[8])


# middle row with most important information

left,middle,right = st.columns(3,vertical_alignment="top",border=True,gap="large")

#left column
with left:

    #temperature,logo,relativetemp, min/max temp daily
    st.subheader(f"{search} Weather")
    with st.container(horizontal=True):
        st.metric(label=f"**Temperature**",value = f"{round(all_weather_info[0],1)}°C",icon = ":material/thermometer:",width="content")
        st.image(weather_icon,width="content")
    st.divider()
    st.markdown(f"Feels like {round(all_weather_info[1],1)}°C")
    st.markdown(f"Daily max temp {all_weather_info[2]}°C")
    st.markdown(f"Daily min temp {all_weather_info[3]}°C")

#middle column
with middle :

    st.metric(label="**Humidity**", value=f"{round(all_weather_info[4], 1)}%", border=True,icon=":material/humidity_mid:")
    st.metric(label="**Wind Speed at 10m height**", value=f"{round(all_weather_info[5], 1)}km/h", border=True,icon=":material/air:")
    st.metric(label="**Precipitation**",value=f"{all_weather_info[9]}mm",border= True, icon = ":material/rainy:")


#right column
with right:

    #Humidity,Wind Speed, UV, sunrise/set

    st.metric(label = "**Sunrise**",value = f"{all_weather_info[6][11:16]}",border = True,icon=":material/wb_twilight:")
    st.metric(label = "**Sunset**",value = f"{all_weather_info[7][11:16]}",border = True,icon=":material/wb_twilight_2:")
    st.metric(label="**UV Value**", value=f"{all_weather_info[16]}", border=True,icon =":material/sunny:")


# weekly weather below the existing current-weather panels
st.subheader("Weekly forecast")
with st.container(horizontal=True, gap="small"):
    for index, day in enumerate(all_weather_info[20]):
        with st.container(border=True, width=150):
            st.markdown("**Today**" if index == 0 else f"**{day['date']:%A}**")
            st.caption(f"{day['date']:%d %b}")
            icon, condition = get_weather_icon(day["weather_code"])
            st.image(icon, width=55)
            st.markdown(condition)
            st.markdown(f"High {format_forecast_value(day['temperature_max'], '°C')}")
            st.caption(f"Low {format_forecast_value(day['temperature_min'], '°C')}")
            st.caption(f"Precipitation  \n{format_forecast_value(day['precipitation'], ' mm')}")


# bottom bar with info
with st.bottom:
    with st.container(border=False, horizontal=True,horizontal_alignment="right"):
        st.link_button(label = "**github**",url = "https://github.com/AdamOl135/Weathercast",type = "tertiary",)

