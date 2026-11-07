# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Homepage",  # The title that appears in the browser tab
    page_icon="🏠",         # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("Welcome to the Data Dashboard! 📊")

# INTRODUCTORY TEXT
st.write("""
This application is designed to collect and visualize data.
You can navigate to the different pages using the sidebar on the left.

### How to use this app:
- **Survey Page**: Go here to input new data into our CSV file.
- **Visuals Page**: Go here to see the data visualized in different graphs.

This project is part of CS 1301's Lab 2.
""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
# st.image("images/welcome_image.png")
# PART 1 INTRODUCTION
st.header("My New Albany Volleyball Stats")
st.write("I played middle hitter for New Albany. This dashboard compares my reported volleyball statistics across three varsity seasons.")
st.write("On the Visuals page, compare kills by season or choose another statistic to explore how the numbers changed.")
st.markdown("[My MaxPreps stats](" + 'https://www.maxpreps.com/oh/new-albany/new-albany-eagles/athletes/yashas-devulapally/volleyball/boys/stats/?careerid=fkomn9is34el5' + ") | [My website](https://yashasdevulapally.com)")
st.caption("Stats come from MaxPreps. The Survey page collects volleyball practice responses, and the Visuals page also charts that survey data.")
