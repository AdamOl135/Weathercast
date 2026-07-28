
import streamlit as st

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

    def search_func():
        st.write("hallo")








# middle row with most important information

x = "assets/PCLOUDY1.png" #weather dependent picture


with st.container():

    # spacing from top
    st.space("large")
    left,right = st.columns([0.7,0.3],vertical_alignment="top")

    #left column
    with left:

        #temperature,logo,relativetemp
        st.markdown("**Current Weather**")
        st.metric(label="Temperature",value = f"{37}°C") #st.image(f"{x}")
        st.write(f"feels like {""} degrees")

    #right column
    with right:

        #Humidity,Wind Speed, UV, sunrise/set
        st.metric(label = "Humidity",value = f"{80}%",border = True)
        st.metric(label = "Wind Speed",value = f"{20}km/h",border=True)
        st.metric(label = "UV",value = f"{7}",border = True)
        st.metric(label = "Sunrise",value = f"{21}",border = True)




# bottom bar with info
with st.bottom:
    with st.container(border=True, horizontal=True):
        st.link_button(label = "github",url = "https://github.com/AdamOl135/Weathercast",type = "tertiary")



