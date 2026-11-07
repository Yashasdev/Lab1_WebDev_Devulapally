# This page collects responses about volleyball practice and saves them to data.csv.

import streamlit as st
import pandas as pd
import csv
import math
from pathlib import Path

st.set_page_config(page_title="Survey", page_icon="📝")

st.title("Volleyball Practice Survey 🏐")
st.write("Which volleyball skill do you practice most, and how many hours did you practice last week?")
st.write("Each response will be saved to the CSV file and included in the charts on the Visuals page.")

# Find the CSV file in the Lab02 folder, even if Streamlit is started elsewhere.
csv_path = Path(__file__).resolve().parent.parent / "data.csv"
skills = ["Serving", "Passing", "Hitting", "Blocking", "Setting"]

with st.form("survey_form"):
    category_input = st.selectbox("Which skill do you practice most?", skills)
    value_input = st.text_input("How many hours did you practice in the past week?", placeholder="Example: 5.5")
    submitted = st.form_submit_button("Submit response")

# Text inputs give us strings. Convert the hours to a number for graphing.
if submitted:
    try:
        hours = float(value_input)
    except ValueError:
        st.error("Please enter a number for practice hours, such as 5 or 5.5.")
    else:
        if not math.isfinite(hours) or hours < 0 or hours > 168:
            st.error("Practice hours must be a number between 0 and 168.")
        else:
            has_header = csv_path.exists() and csv_path.stat().st_size > 0
            with open(csv_path, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not has_header:
                    writer.writerow(["Category", "Value"])
                writer.writerow([category_input, hours])
            st.success("Your response was saved to data.csv!")
            st.write(f"Skill: **{category_input}** | Practice hours: **{hours:g}**")

st.divider()
st.header("Responses saved so far")
if csv_path.exists() and csv_path.stat().st_size > 0:
    saved_data = pd.read_csv(csv_path)
    if saved_data.empty:
        st.info("No survey responses yet. Submit the form above to add the first one.")
    else:
        st.dataframe(saved_data, hide_index=True)
        st.caption(f"Total responses: {len(saved_data)}")
else:
    st.info("No responses yet. Submit the form above to create the CSV file.")
