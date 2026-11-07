# This creates the page for displaying data visualizations.

import streamlit as st
import json
from pathlib import Path
import pandas as pd
import altair as alt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")

# PART 1: GRAPHS FROM data.json
json_path = Path(__file__).resolve().parent.parent / "data.json"
with open(json_path) as file:
    volleyball = json.load(file)

st.header(volleyball["chart_title"])
st.caption(volleyball["source"])
st.markdown(f"[Source: MaxPreps]({volleyball['source_url']}) | [My website]({volleyball['profile_url']})")
st.caption(f"MaxPreps last updated: {volleyball['source_last_updated']}. Data retrieved: {volleyball['retrieved_on']}.")
seasons = pd.DataFrame(volleyball["data_points"])
st.dataframe(seasons, hide_index=True)

# Static chart: every season is included regardless of the controls below.
st.subheader("My kills by season")
bar_chart = alt.Chart(seasons).mark_bar(color="#245b83").encode(
    x=alt.X("season:O", title="Varsity season", sort=list(seasons["season"])),
    y=alt.Y("kills:Q", title="Total kills"),
    tooltip=["season", "kills", "sets"]
).properties(title="Reported kills across three varsity seasons")
st.altair_chart(bar_chart, width="stretch")
st.write(f"I recorded {int(seasons['kills'].sum())} kills across {int(seasons['sets'].sum())} sets in these seasons.")
st.caption("Season totals depend partly on how many sets were played. They do not measure performance per set.")

# Dynamic chart: the selected statistic stays in session state between reruns.
st.subheader("Compare my season statistics")
labels = {"kills": "Kills", "sets": "Sets played", "attempts": "Attack attempts",
          "errors": "Attack errors", "hitting_percentage": "Hitting percentage"}
if "selected_stat" not in st.session_state:
    st.session_state["selected_stat"] = "kills"
st.selectbox("Choose a statistic", list(labels), format_func=lambda stat: labels[stat],
             key="selected_stat")
stat = st.session_state["selected_stat"]
line_chart = alt.Chart(seasons).mark_line(point=True).encode(
    x=alt.X("season:O", title="Varsity season", sort=list(seasons["season"])),
    y=alt.Y(f"{stat}:Q", title=labels[stat], scale=alt.Scale(zero=True)),
    tooltip=["season", stat]
).properties(title=f"{labels[stat]} across my varsity seasons")
st.altair_chart(line_chart, width="stretch")
mean = float(seasons[stat].mean())
median = float(seasons[stat].median())
precision = 3 if stat == "hitting_percentage" else 2
left, right = st.columns(2)
left.metric("Mean across seasons", f"{mean:.{precision}f}")
right.metric("Median across seasons", f"{median:.{precision}f}")
st.caption("These summaries update with the selected statistic. Each season has equal weight. Hitting percentage is shown as a decimal; its mean here is not the career hitting percentage.")

# PART 2: GRAPHS FROM data.csv
st.divider()
st.header("Volleyball Practice Survey Results")
st.write("These charts use the responses saved from the Survey page, not the season statistics in data.json.")

csv_path = Path(__file__).resolve().parent.parent / "data.csv"
if csv_path.exists() and csv_path.stat().st_size > 0:
    practice = pd.read_csv(csv_path)
else:
    practice = pd.DataFrame(columns=["Category", "Value"])

if not {"Category", "Value"}.issubset(practice.columns):
    st.error("data.csv needs Category and Value columns.")
else:
    # Clean up the hours column in case someone edits the CSV manually.
    practice["Value"] = pd.to_numeric(practice["Value"], errors="coerce")
    practice = practice.dropna(subset=["Category", "Value"])
    practice = practice[(practice["Value"] >= 0) & (practice["Value"] <= 168)].copy()
    skills = ["Serving", "Passing", "Hitting", "Blocking", "Setting"]
    practice = practice[practice["Category"].isin(skills)].copy()

    if practice.empty:
        st.info("There are no survey responses yet. Open Survey, submit some answers, and return to see both charts.")
    else:
        # Each CSV row represents one submitted survey response.
        practice["Response"] = list(range(1, len(practice) + 1))
        st.caption(f"Survey responses collected: {len(practice)}")

        # Static chart: counts of all reported most-practiced skills.
        st.subheader("Most practiced volleyball skills")
        counts = practice["Category"].value_counts().reindex(skills, fill_value=0)
        counts = counts.rename_axis("Category").reset_index(name="Responses")
        skill_chart = alt.Chart(counts).mark_bar(color="#3e7771").encode(
            x=alt.X("Category:N", title="Volleyball skill", sort=skills),
            y=alt.Y("Responses:Q", title="Number of responses", axis=alt.Axis(tickMinStep=1)),
            tooltip=["Category", "Responses"]
        ).properties(title="Most-practiced skill reported by survey participants")
        st.altair_chart(skill_chart, width="stretch")
        st.caption("This chart always includes every valid response and does not depend on the selection below.")

        # Dynamic chart: the dropdown changes which survey responses are plotted.
        st.subheader("Practice hours by response")
        skill_options = ["All skills"] + skills
        if "survey_selected_skill" not in st.session_state:
            st.session_state["survey_selected_skill"] = "All skills"
        st.selectbox("Choose which skill to display", skill_options, key="survey_selected_skill")
        selected_skill = st.session_state["survey_selected_skill"]
        if selected_skill == "All skills":
            selected_data = practice
        else:
            selected_data = practice[practice["Category"] == selected_skill]

        if selected_data.empty:
            st.info("No responses for this skill yet. Choose another skill or submit a new response.")
        else:
            hours_chart = alt.Chart(selected_data).mark_circle(size=120).encode(
                x=alt.X("Response:Q", title="Survey response number", axis=alt.Axis(tickMinStep=1)),
                y=alt.Y("Value:Q", title="Practice hours in the past week", scale=alt.Scale(zero=True)),
                color=alt.Color("Category:N", title="Most-practiced skill"),
                tooltip=[
                    alt.Tooltip("Response:Q", title="Response"),
                    alt.Tooltip("Category:N", title="Skill"),
                    alt.Tooltip("Value:Q", title="Hours practiced")
                ]
            ).properties(title=f"Practice hours: {selected_skill}")
            st.altair_chart(hours_chart, width="stretch")

            # Extra credit: these metrics change as the chosen skill changes.
            mean_hours = selected_data["Value"].mean()
            median_hours = selected_data["Value"].median()
            mean_col, median_col = st.columns(2)
            mean_col.metric("Mean practice hours", f"{mean_hours:.2f}")
            median_col.metric("Median practice hours", f"{median_hours:.2f}")
            st.caption("The mean and median are calculated only from the responses shown in this scatter plot.")
