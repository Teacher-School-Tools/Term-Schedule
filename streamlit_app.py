import streamlit as st
from term_schedule import load_lessons, load_misc_days, create_schedule, gen_calendar, parse_settings

st.set_page_config(layout="wide")

sample_lessons = r"""Introduction
Diagnostic Quiz [#aa6767]
Polynomials [3]
Exponentials [2]
Polynomial Quiz [q]
Factoring
Completing the Square [2]
Word Problems [2]
Review
Quadratics Test [t]
Introduction to Trigonometry
Angle Patterns
Right Angle Triangles
"""

sample_holidays = r"""2026-9-11 : PD Day 1
2026-9-18 : Field Trip
2026-9-25 : School Assembly
"""

webpage_text = rf"""
## What is this?
This is a tool that will automatically generate a calendar based on your inputted lessons, days required for each lesson, and will account for holidays / flex days based on the current calendar year.
## How to use
You will need two pieces of information. Your lesson titles, and school-board specific holidays

Simply provide a text form of your lesson plans in order, similar to the following.
```
{sample_lessons}
```
Note a couple different features above. Numbers in square brackets such as `[3]` indicate a lesson which spans more than one day. Hex-codes within square brackets such as `[#aa6767]` indicate a custom colour for the specific day. You can choose any colour provided that you know the hex-code for. You can also indicate if a day is a quiz or test day with `[q]` or `[t]`

The second thing you need is a list of the PD days for your specific board. I may implement a library of schoolboard days in another iteration.

It should look something like the following.

```
{sample_holidays}
```"""

# calendar generation helper function
def main():
    fig, ax = gen_calendar(df, config_settings=settings)

    st.pyplot(fig, width="stretch")

# STREAMLIT CONTENT STARTS BELOW HERE

# sidebar content
side = st.sidebar
with side:
    disable_mode = False
    st.markdown("""
    # Advanced Settings
    """)
    reset_button = st.button("Reset Settings")
    STAT_HOLIDAY_COLOUR = st.color_picker("Select the colour for statutory holidays", 
                                                key="1", value="#FFB6A6",
                                                )
    SCHOOL_HOLIDAY_COLOUR = st.color_picker("Select the colour for school holidays", 
                                                key="2", value="#399E4A")
    DEFAULT_INSTR_DAY_COLOUR = st.color_picker("Select the colour for default instructional days", 
                                                key="3", value="#67A2C5")

    DEFAULT_TEST_COLOUR = st.color_picker("Select the colour for quiz days", 
                                                key="4", value="#9BCEC1")
    DEFAULT_QUIZ_COLOUR = st.color_picker("Select the colour for test days", 
                                                key="5", value="#FFC349")
    
    expand = st.expander("""Size Settings""")

    with expand:
        st.markdown("Warning: Changing some of the sizes can and will break the calendar! Do so at your own risk!")
        gap_size = st.number_input("Gap size",          key="6", value=50)
        round_size = st.number_input("Round size",      key="7", value=50)
        rect_x_size = st.number_input("Cell x-size",    key="8", value=1000,)
        rect_y_size = st.number_input("Cell y-size",    key="9", value=rect_x_size//2)
        cell_border_size = st.number_input("Cell border size", key="10", value=2)
        figure_border_size = st.number_input("Border Size",    key="11", value=3)
        text_offset_x = st.number_input("Number Offset x",  key="12", value=0)
        text_offset_y = st.number_input("Number Offset y",  key="13", value=0)
        dark_mode_check = st.checkbox("Darkmode",       key="14", value=False)

    custom_settings = st.text_area("Paste your settings from the previous session to use them again. If there are settings here, they will be prioritized over the settings above!")

    if custom_settings:
        disable_mode = True
        settings = parse_settings(custom_settings)
        # for k in st.session_state.keys():
        #     st.session_state[k] = not st.session_state[k].disabled


    else:
        disable_mode = False
        settings = {
            "weekends" : False,
            "gap" : gap_size,
            "round" : round_size,
            "rect_x" : rect_x_size,
            "rect_y" : rect_y_size,
            "cell_border" : cell_border_size,
            "stat_holiday_colour" : STAT_HOLIDAY_COLOUR.capitalize(),
            "school_holiday_colour" : SCHOOL_HOLIDAY_COLOUR.capitalize(),
            "default_day_colour" : DEFAULT_INSTR_DAY_COLOUR.capitalize(),
            "default_quiz_colour" : DEFAULT_QUIZ_COLOUR.capitalize(),
            "default_test_colour" : DEFAULT_TEST_COLOUR.capitalize(),
            "figure_border_size" : figure_border_size,
            "text_offset_x" : text_offset_x,
            "text_offset_y" : text_offset_y,
            "dark_mode" : dark_mode_check,
        }

    tmp = ""

    for k,v in zip(settings.keys(), settings.values()):
        tmp += f"{k} : {v},"

    st.markdown(fr"""
    Copy the following and save it somewhere if you want to reuse the same settings in your next session, or if you refresh the page.
    ```
    {tmp}
    ```
    """)

    if reset_button:
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

import matplotlib.pyplot as plt
plt.rc('font', size=10)
plt.rc('axes', titlesize=20)

# main content - three columns
st.markdown("# Term Planner", text_alignment="center")

left_column, mid_column, right_column  = st.columns(3, gap="medium")

with left_column:

    st.markdown(webpage_text)

with mid_column:
    st.markdown("## Inputs")
    
    col1, col2 = st.columns(2)

    with col1:
        lessons_input = st.text_area("Input your lesson schedule here:",
                                    value=sample_lessons)

        loaded_lessons = load_lessons(lessons_input, settings)

    with col2:
        holidays = st.text_area("Input your school holidays / flex days here:",
                                value=sample_holidays)
        
        misc_days = None
        try:
            misc_days = load_misc_days(holidays)
        except ValueError:
            pass

    start_date = st.date_input("Select the starting date for the term.", value="2026-09-07")

    df = create_schedule(loaded_lessons, misc_days, settings, start_date=str(start_date))

    st.markdown("Below is a table of your data. You can use this as a general guideline for your students, excluding the dates, as it may change from term-to-term.")
    st.dataframe(df)

if not loaded_lessons or not misc_days:
    pass

else:
    with right_column:
        st.markdown("""
        ## Output
        To save the calendar, simply right click the image and click "Save image as...\"""""")
        main()

