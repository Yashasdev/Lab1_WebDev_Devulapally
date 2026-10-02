import streamlit as st


st.title("Explore Your Biomedical Engineering Strengths")
st.write(
    "Answer these questions about your interests and working style. You will get "
    "one of three possible matches: biomedical researcher, medical device designer, "
    "or STEM educator and innovator. This quiz is for exploration, not career advice."
)

st.subheader("1. Which challenge would you most like to work on?")
challenge = st.radio(
    "Choose one:",
    [
        "Understanding what is happening inside the body",
        "Designing a device that helps someone move or recover",
        "Helping students learn engineering by building things",
    ],
)  #NEW

st.image("Images/research.jpg", caption="Biomedical research and imaging")

st.subheader("2. Which activities sound interesting to you?")
activities = st.multiselect(
    "Select all that apply:",
    [
        "Analyzing images or data",
        "Building and testing prototypes",
        "Teaching or mentoring",
        "Talking with people about a problem",
        "Planning a project or startup",
    ],
)  #NEW

st.subheader("3. How much do you enjoy hands-on building?")
hands_on = st.slider("Rate your interest", min_value=1, max_value=10, value=5)  #NEW

st.image("Images/intern.jpg", caption="Learning through hands-on research")

st.subheader("4. Where would you most like to spend a project day?")
setting = st.selectbox(
    "Pick a setting:",
    ["A research lab", "A design workshop", "A classroom or community program"],
)  #NEW

st.subheader("5. How many hours per week would you want to spend mentoring others?")
mentoring_hours = st.number_input(
    "Hours per week", min_value=0, max_value=20, value=2, step=1
)  #NEW

st.image("Images/tlae.jpg", caption="STEM education and hands-on engineering")

if st.button("Show my match"):
    research_score = 0
    design_score = 0
    education_score = 0

    if challenge == "Understanding what is happening inside the body":
        research_score += 2
    elif challenge == "Designing a device that helps someone move or recover":
        design_score += 2
    else:
        education_score += 2

    if "Analyzing images or data" in activities:
        research_score += 1
    if "Building and testing prototypes" in activities:
        design_score += 1
    if "Teaching or mentoring" in activities:
        education_score += 1
    if "Talking with people about a problem" in activities:
        design_score += 1
        education_score += 1
    if "Planning a project or startup" in activities:
        design_score += 1
        education_score += 1

    if hands_on >= 7:
        design_score += 2
    elif hands_on <= 3:
        research_score += 1

    if setting == "A research lab":
        research_score += 2
    elif setting == "A design workshop":
        design_score += 2
    else:
        education_score += 2

    if mentoring_hours >= 6:
        education_score += 2
    elif mentoring_hours == 0:
        research_score += 1
        design_score += 1

    top_score = max(research_score, design_score, education_score)

    # Use the first answer to choose the result if the highest scores are tied.
    if challenge == "Understanding what is happening inside the body" and research_score == top_score:
        match = "Biomedical Researcher"
        image_path = "Images/research.jpg"
        explanation = (
            "You are drawn to asking questions, studying evidence, and using data "
            "to understand health and disease. You might enjoy biomedical imaging, "
            "lab research, or clinical research projects."
        )
    elif challenge == "Designing a device that helps someone move or recover" and design_score == top_score:
        match = "Medical Device Designer"
        image_path = "Images/intern.jpg"
        explanation = (
            "You like turning a real need into something people can test and use. "
            "You might enjoy prototyping, biomechanics, rehabilitation engineering, "
            "or medical device development."
        )
    elif challenge == "Helping students learn engineering by building things" and education_score == top_score:
        match = "STEM Educator and Innovator"
        image_path = "Images/tlae.jpg"
        explanation = (
            "You are energized by sharing ideas and helping others build confidence. "
            "You might enjoy STEM outreach, educational technology, or creating "
            "programs that make engineering accessible."
        )
    elif research_score == top_score:
        match = "Biomedical Researcher"
        image_path = "Images/research.jpg"
        explanation = (
            "You are drawn to asking questions, studying evidence, and using data "
            "to understand health and disease. You might enjoy biomedical imaging, "
            "lab research, or clinical research projects."
        )
    elif design_score == top_score:
        match = "Medical Device Designer"
        image_path = "Images/intern.jpg"
        explanation = (
            "You like turning a real need into something people can test and use. "
            "You might enjoy prototyping, biomechanics, rehabilitation engineering, "
            "or medical device development."
        )
    else:
        match = "STEM Educator and Innovator"
        image_path = "Images/tlae.jpg"
        explanation = (
            "You are energized by sharing ideas and helping others build confidence. "
            "You might enjoy STEM outreach, educational technology, or creating "
            "programs that make engineering accessible."
        )

    st.success(f"Your match: {match}")
    st.write(explanation)
    st.image(image_path, caption=match)
    st.metric("Points in your strongest category", top_score)  #NEW
#Extra credit progress bar
    st.subheader("Your score breakdown")
    st.bar_chart(
        {
            "Biomedical Researcher": research_score,
            "Medical Device Designer": design_score,
            "STEM Educator and Innovator": education_score,
        }
    )
