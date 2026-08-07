import streamlit as st
from weather import get_city


#top row with logo, app name and search function
with st.container(horizontal=True, horizontal_alignment = "distribute",width="stretch"):

    #logo & Title
    logo = st.image("assets/PCLOUDY1.png",width = 30,output_format="PNG")
    name = st.text("Weathercast")

    #spacing between elements
    st.space("stretch")


    #search button for city with max input as safety precaution
    search = st.text_input(label = "placeholder", label_visibility="collapsed", max_chars=100,
                               placeholder= "Search for City",persist_state= "page",key="CityInput",disabled=False,)
    st.text(search)

    if search == None:
        default_weather_info = get_city("Berlin")
    else:
        all_weather_info = get_city(search)





# middle row with most important information

x = "assets/PCLOUDY1.png" #weather dependent picture

with st.container():

    # spacing from top
    st.space("large")
    left,right = st.columns([0.5,0.5],vertical_alignment="top")

    #left column
    with left:

        #temperature,logo,relativetemp, min/max temp daily
        st.subheader(f"{search} Weather")
        st.metric(label="Temperature",value = f"{round(all_weather_info[0],1)}°C") #st.image(f"{x}")
        st.markdown(f"Feels like {round(all_weather_info[1],1)}°C")
        st.markdown(f"Daily max temp {all_weather_info[2]}°C")
        st.markdown(f"Daily min temp {all_weather_info[3]}°C")


    #right column
    with right:

        #Humidity,Wind Speed, UV, sunrise/set
        st.metric(label = "Humidity",value = f"{round(all_weather_info[4],1)}%",border = True)
        st.metric(label = "Wind Speed at 10m height",value = f"{round(all_weather_info[5],1)}km/h",border=True)
        st.metric(label = "UV",value = f"{""}",border = True)
        st.metric(label = "Sunrise",value = f"{all_weather_info[6][11:16]}",border = True)
        st.metric(label = "Sunset",value = f"{all_weather_info[7][11:16]}",border = True)


# bottom bar with info
with st.bottom:
    with st.container(border=True, horizontal=True):
        st.link_button(label = "github",url = "https://github.com/AdamOl135/Weathercast",type = "tertiary")

