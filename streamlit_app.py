import streamlit as st

st.write("Select one of the apps to use.")

if st.button("Go to Scheduler"):
    st.switch_page("pages/0_term_schedule_app.py")

if st.button("Go to Randomizer"):
    st.switch_page("pages/1_group_randomizer_app.py")