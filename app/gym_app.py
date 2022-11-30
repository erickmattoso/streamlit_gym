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
    .css-18e3th9 {padding: 3rem 5rem 10rem;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    page_settings()

def page_settings():
    def fetch_and_clean_data1(file_):
        current_directory = Path(__file__).parent
        file = open(os.path.join(current_directory, file_), 'rb')
        df = pd.read_csv(file)
        return df

    @st.cache(allow_output_mutation=True)
    def get_data():
        return []

    #read data
    df_exercises = fetch_and_clean_data1('exercises.csv')
    #define cols
    row1, row2, row3 = st.columns([1, 1, 1])
    #display first day where status = todo
    day = df_exercises[df_exercises["Status"] == "ToDo"]["index"].values[0]
    # filter based first day = todo
    day = row1.number_input("label", min_value=1, max_value=84, value=day)
    sts = row2.selectbox("Status", options=("Done", "ToDo"))
    df_exer_html = df_exercises[df_exercises["index"] == day]
    stz = df_exercises[df_exercises["index"] == day]["Status"].values[0]
    title = ("Exercises: Day ", str(day), stz)
    st.title(' '.join(title))
    if row3.button("Update"):
        df_exercises.loc[(df_exercises["index"] == day), "Status"] = sts
        df_exercises.to_csv('app/exercises.csv', index=0)

    # display table columns
    cols = st.columns((0.25, 1, 1, 1, 1, 1, 1))
    cols[2].subheader("Week")
    cols[3].subheader("Exercise")
    cols[4].subheader("Sets")
    cols[5].subheader("Reps")
    cols[6].subheader("obs")


    #display table content
    repeat = len(df_exer_html)
    for i in range(repeat):
        cols = st.columns((0.25, 1, 1, 1, 1, 1, 1))
        st.markdown("""---""")
        j = df_exer_html["Unnamed: 0"].values[i]
        cols[0].checkbox(f'{j}')
        try:
            cols[1].image(df_exer_html["image"].values[i])
        except:
            pass
        cols[2].write(str(df_exer_html["Week"].values[i]))
        cols[3].write(str(df_exer_html["Exercise"].values[i]))
        cols[4].write(str(df_exer_html["Sets"].values[i]))
        cols[5].write(str(df_exer_html["Reps"].values[i]))
        text = cols[6].text_area(f'{j}.Obs', value=df_exercises["comments"][j])

        if cols[6].button(f'{j}.Save'):  
            df_exercises.loc[(df_exercises["Unnamed: 0"] == j), "comments"] = text
            df_exercises.to_csv('app/exercises.csv', index=0)
            cols[6].write("Saved!")


    st.title("The 3000 Calorie diet meal plan")
    df_nutrition = fetch_and_clean_data1('food2.csv')
    df_by_day = df_nutrition[df_nutrition["day"] == int(day)]
    labels = ["Calories", "Carbs", "Fat", "Protein", "Fiber"]
    nutri_values = df_by_day[labels].sum(axis=0)
    fig1, ax1 = plt.subplots()
    Colours = ["#fd7e14", "#ffc107", "#20c997", "#6f42c1", "#28a745"]
    ax1.pie(nutri_values, labels=labels, autopct="%1.1f%%",
            startangle=90, colors=Colours)
    ax1.axis("equal")
    tt = df_by_day[["type_meal", "Meal", "Portion"] +
                    labels].reset_index(drop=True)
    tt = tt.to_html(escape=False)
    total_cal = df_by_day["Calories"].sum()
    st.write(f"This plan contains {total_cal} calories")
    row1, row2 = st.columns([3, 1])
    row1.write(tt, unsafe_allow_html=True)
    row2.pyplot(fig1)

if __name__ == "__main__":
    main()