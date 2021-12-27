import pandas as pd
import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
# Import Libs
from folium.plugins import FastMarkerCluster
from st_aggrid import AgGrid, GridUpdateMode, GridOptionsBuilder
import base64
import folium
import io
import pandas as pd
import seaborn as sns
import streamlit as st


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

    def fetch_and_clean_data1(file):
        df = pd.read_csv(file, index_col=[0])
        return df
    df_exercises = fetch_and_clean_data1('exercises.csv')
    today = st.sidebar.date_input("Date", date.today())
    df_exer_html = df_exercises[df_exercises["Date"]
                                == today.strftime("%Y-%m-%d")]
    try:
        days = df_exer_html["index"].sample().values[0].astype(str)
        st.write(f"Day number {days}")
        df_exer_html = df_exer_html[[
            "image",
            "Week",
            "Exercise",
            "Sets",
            "Reps",
            "obs"
        ]].reset_index(drop=True).to_html(escape=False)
        st.write(df_exer_html, unsafe_allow_html=True)
        st.text(" \n")
        st.text(" \n")
        st.title("The 3000 Calorie diet meal plan")
        df_nutrition = fetch_and_clean_data1('food.csv')
        df_by_day = df_nutrition[df_nutrition["day"] == int(days)]
        labels = ["Calories", "Carbs", "Fat", "Protein", "Fiber"]
        nutri_values = df_by_day[labels].sum(axis=0)

        fig1, ax1 = plt.subplots()
        Colours = ["#fd7e14", "#ffc107", "#20c997", "#6f42c1", "#28a745"]
        ax1.pie(nutri_values, labels=labels, autopct="%1.1f%%",
                startangle=90, colors=Colours)
        ax1.axis("equal")
        df_by_day["Meal"] = "<a href=" + \
            df_by_day["receita"]+">"+df_by_day["meal"]+"</a>"
        tt = df_by_day[["type_meal", "Meal"] +
                       labels].reset_index(drop=True).to_html(escape=False)
        row1, row2 = st.columns([2, 1])
        row1.write(tt, unsafe_allow_html=True)
        row2.pyplot(fig1)
        row2.text(df_by_day["Calories"].sum())

    except:
        minimo = df_exercises["Date"].min()
        maximo = df_exercises["Date"].max()
        st.write(f"You should look between {minimo} and {maximo}.")


if __name__ == "__main__":
    main()
