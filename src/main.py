import streamlit as st
import weather



#top row with logo, app name and search function
with st.container(horizontal=True, horizontal_alignment = "distribute",width="stretch"):

    #logo & Title
    logo = st.image("assets/PCLOUDY1.png",width = 30,output_format="PNG")
    name = st.markdown("***Weathercast***")

    #spacing between elements
    st.space("stretch")


    #search button for city with max input as safety precaution
    search = st.text_input(label = "placeholder", label_visibility="collapsed", max_chars=100,
                           placeholder= "Search for City",persist_state= "page",key="CityInput",disabled=False)

    st.text(search)




# middle row with most important information

x = "assets/PCLOUDY1.png" #weather dependent picture


with st.container():

    # spacing from top
    st.space("large")
    left,right = st.columns([0.5,0.5],vertical_alignment="top")

    #left column
    with left:

        #temperature,logo,relativetemp
        st.markdown("**Current Weather**")
        st.metric(label="Temperature",value = f"{round(weather.weather_data.current_temperature,1)}°C") #st.image(f"{x}")
        st.write(f"feels like {round(weather.weather_data.current_apparent_temperature,1)} degrees")

    #right column
    with right:

        #Humidity,Wind Speed, UV, sunrise/set
        st.metric(label = "Humidity",value = f"{round(weather.weather_data.current_relative_humidity,1)}%",border = True)
        st.metric(label = "Wind Speed",value = f"{round(weather.weather_data.current_wind_speed,1)}km/h",border=True)
        st.metric(label = "UV",value = f"{""}",border = True)
        st.metric(label = "Sunrise",value = f"{weather.weather_data.daily_sunrise_gmtime_adjusted[11:16]}",border = True)
        st.metric(label = "Sunset",value = f"{weather.weather_data.daily_sunset_gmtime_adjusted[11:16]}",border = True)




# bottom bar with info
with st.bottom:
    with st.container(border=True, horizontal=True):
        st.link_button(label = "github",url = "https://github.com/AdamOl135/Weathercast",type = "tertiary")

