import streamlit as st
from weather import get_city

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
    logo = st.image(image="assets/PCLOUDY1.png",width = 35,output_format="PNG")
    name = st.subheader(body="Weathercast",text_alignment="left",divider="grey")

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


    all_weather_info = get_city(search)

    st.text(type(all_weather_info))

    weather_icon = ""

    #checking weather condition and changing icon based on it
    if all_weather_info[8] == 0.0:
        weather_icon = "assets/CLEAR0.png"
    elif all_weather_info[8] == 1.0:
        weather_icon = "assets/CLEAR1.png"
    elif all_weather_info[14] > 76 and all_weather_info[9] > 2.4 :
        weather_icon = "assets/HAIL.png"
    # first 3




#todo : seperated words cannot be input into search, fix


# middle row with most important information




# spacing from top
st.space("large")

left,middle,right = st.columns(3,vertical_alignment="top",border=True,gap="large")

#left column
with left:

    #temperature,logo,relativetemp, min/max temp daily
    st.subheader(f"{search} Weather")
    with st.container(horizontal=True):
        st.metric(label=f"**Temperature**",value = f"{round(all_weather_info[0],1)}°C",icon = ":material/thermometer:",width="content")
        #st.text("affe")
        st.image(weather_icon,width="content")
    st.markdown(f"Feels like {round(all_weather_info[1],1)}°C")
    st.markdown(f"Daily max temp {all_weather_info[2]}°C")
    st.markdown(f"Daily min temp {all_weather_info[3]}°C")

with middle :
    st.metric(label="**Humidity**", value=f"{round(all_weather_info[4], 1)}%", border=True)
    st.metric(label="**Wind Speed at 10m height**", value=f"{round(all_weather_info[5], 1)}km/h", border=True)
    st.metric(label="**UV**", value=f"{""}", border=True)


#right column
with right:

    #Humidity,Wind Speed, UV, sunrise/set

    st.metric(label = "**Sunrise**",value = f"{all_weather_info[6][11:16]}",border = True)
    st.metric(label = "**Sunset**",value = f"{all_weather_info[7][11:16]}",border = True)


# bottom bar with info
    with st.bottom:
        with st.container(border=True, horizontal=True):
            st.link_button(label = "github",url = "https://github.com/AdamOl135/Weathercast",type = "tertiary")

