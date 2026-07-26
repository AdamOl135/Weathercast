import streamlit as st

with st.sidebar:
    logo = st.image("assets/PCLOUDY1.png",width= 30)



#top row with logo, app name and search function
with st.container(horizontal=True, horizontal_alignment = "distribute",width="stretch"):

    #logo & Title
    logo = st.image("assets/PCLOUDY1.png",width= 30)
    name = st.markdown("**Weathercast**")

    #spacing between elements
    st.space("stretch")

    #search button for city with max input as safety precaution
    search = st.text_input(label = "placeholder", label_visibility="collapsed", max_chars=100,
                           placeholder= "Search for City")
