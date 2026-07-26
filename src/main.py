import streamlit as st


with (st.container(border = True,horizontal=True, horizontal_alignment = "distribute")):

    logo = st.image("assets/PCLOUDY1.png")
    name = st.write("Weathercast")
    search = st.write("search")



#todo : bugfix for logo (lots of code shows up out of nowhere)