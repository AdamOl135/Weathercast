import streamlit as st

st.title("title")


# top row with logo, app name and search function
with (st.container(border = True,horizontal=True, horizontal_alignment = "distribute",width="stretch")):



    logo = st.image("assets/PCLOUDY1.png",width= 30)
    logo.space = ("stretch")
    name = st.write("Weathercast")

    #spacing between elements
    st.space("stretch")

    #search button for city with max input as safety precaution
    search = st.text_input(label="search for city",max_chars=100)
