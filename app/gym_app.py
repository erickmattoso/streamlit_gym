import pandas as pd
import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
from pathlib import Path
import os


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

    def fetch_and_clean_data1(file_):
        current_directory = Path(__file__).parent
        file = open(os.path.join(current_directory, file_), 'rb')
        df = pd.read_csv(file)
        return df

    df_exercises = fetch_and_clean_data1('exercises.csv')
    today = st.sidebar.date_input("Date", date.today())  # st.sidebar.
    st.sidebar.markdown(
        "[Source](https://www.muscleandfitness.com/routine/workouts/workout-routines/reform-90-day-transformation-program-every-man/)")

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
            "obs",
        ]].reset_index(drop=True).to_html(escape=False)
        st.write(df_exer_html, unsafe_allow_html=True)
        st.text(" \n")
        st.text(" \n")
        st.title("The 3000 Calorie diet meal plan")
        df_nutrition = fetch_and_clean_data1('food2.csv')
        df_by_day = df_nutrition[df_nutrition["day"] == int(days)]
        labels = ["Calories", "Carbs", "Fat", "Protein", "Fiber"]
        nutri_values = df_by_day[labels].sum(axis=0)
        fig1, ax1 = plt.subplots()
        Colours = ["#fd7e14", "#ffc107", "#20c997", "#6f42c1", "#28a745"]
        ax1.pie(nutri_values, labels=labels, autopct="%1.1f%%",
                startangle=90, colors=Colours)
        ax1.axis("equal")
        tt = df_by_day[["type_meal", "Meal", "Portion"] +
                       labels].reset_index(drop=True)
        tt = tt.to_html(escape=False)  # , col_space=5)
        total_cal = df_by_day["Calories"].sum()
        st.write(f"This plan contains {total_cal} calories")

        row1, row2 = st.columns([3, 1])
        row1.write(tt, unsafe_allow_html=True)
        row2.pyplot(fig1)

    except:
        minimo = df_exercises["Date"].min()
        maximo = df_exercises["Date"].max()
        st.write(f"You should look between {minimo} and {maximo}.")


if __name__ == "__main__":
    main()
