import pandas as pd
import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
from pathlib import Path
import os
from streamlit import caching


def main():
    st.set_page_config(layout="wide")
    hide_streamlit_style = """
    <style>
    # MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-18e3th9 {padding: 1rem 5rem 10rem;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    page_settings()


def page_settings():
    st.title("90 days chalenge")

    @st.cache(allow_output_mutation=True)
    def get_data():
        return []

    val = [item for sublist in get_data() for item in sublist]
    user_id = st.multiselect("Add Here",['Hardik','Rohit', 'Rahul', 'Virat', 'Pant'], val)
    row1,row2,row3 = st.columns([1,1,8])
    st.write(val)
    st.write(user_id)
    st.write(get_data())

    if row1.button("Remove item"):
        get_data().clear()
        get_data().append(user_id)

    if row2.button("Clear cache"):
        get_data().clear()


if __name__ == "__main__":
    main()