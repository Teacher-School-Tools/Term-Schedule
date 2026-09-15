import streamlit as st

pages = [
    st.Page("pages/0_term_schedule_app.py", title="Scheduler"),
    st.Page("pages/1_group_randomizer.py", title="Randomizer"),
]

pg = st.navigation(pages)

st.write("Select one of the apps to use.")

if st.button("Go to Scheduler"):
    st.switch_page("pages/0_term_schedule_app.py")

if st.button("Go to Randomizer"):
    st.switch_page("pages/1_group_randomizer_app.py")