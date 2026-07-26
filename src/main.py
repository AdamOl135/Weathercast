import streamlit as st


with (st.container(border = True,horizontal=True, horizontal_alignment = "distribute")):

    logo = st.image("PCLOUDY1.png")
    name = "Weathercast"
    search = "search"

    st.write(logo)
    st.write(name)
    st.write(search)
