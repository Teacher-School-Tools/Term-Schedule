import random
import string
import streamlit as st

st.set_page_config(
    page_title="Student Group Generator",
    page_icon="👥",
    layout="wide"
)

# Custom CSS for larger text
st.markdown(
    """
    <style>
        /* Make student names larger */
        .student-name {
            font-size: 28px;
            font-weight: 500;
            margin-bottom: 8px;
        }

        /* Make group headings larger */
        .group-title {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 15px;
        }

        /* Make captions slightly larger */
        .student-count {
            font-size: 18px;
            color: #666;
        }

        /* Add some spacing around groups */
        .group-container {
            padding: 10px 15px 20px 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("👥 Random Student Group Generator")
st.write(
    "Enter your students, choose the number of groups, "
    "and randomly assign them."
)


# ---------------------------------------------------------
# Student input
# ---------------------------------------------------------

student_text = st.text_area(
    "Student Names",
    placeholder=(
        "Enter one student per line:\n\n"
        "Alice\n"
        "Bob\n"
        "Charlie\n"
        "Diana\n"
        "Ethan"
    ),
    height=250
)


# ---------------------------------------------------------
# Number of groups
# ---------------------------------------------------------

num_groups = st.number_input(
    "Number of Groups",
    min_value=1,
    max_value=50,
    value=3,
    step=1
)


# ---------------------------------------------------------
# Clean student names
# ---------------------------------------------------------

def clean_student_name(name):
    """
    Remove punctuation from a student name.

    Examples:
        '"John Smith"'  -> 'John Smith'
        "'Jane Doe'"    -> 'Jane Doe'
        "Alex!"         -> 'Alex'
        "Sam (Student)" -> 'Sam Student'
    """

    # Remove ALL ASCII punctuation
    name = name.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Remove extra whitespace
    name = " ".join(name.split())

    return name.strip()


# ---------------------------------------------------------
# Create groups
# ---------------------------------------------------------

def create_groups(students, number_of_groups):
    """Randomly distribute students as evenly as possible."""

    shuffled_students = students.copy()
    random.shuffle(shuffled_students)

    groups = [[] for _ in range(number_of_groups)]

    for index, student in enumerate(shuffled_students):
        groups[index % number_of_groups].append(student)

    return groups


# ---------------------------------------------------------
# Initialize session state
# ---------------------------------------------------------

if "groups" not in st.session_state:
    st.session_state.groups = None


# ---------------------------------------------------------
# Randomize button
# ---------------------------------------------------------

if st.button(
    "🎲 Randomize Groups",
    type="primary",
    use_container_width=True
):

    # Process each line
    students = [
        clean_student_name(name)
        for name in student_text.splitlines()
    ]

    # Remove blank entries
    students = [
        name for name in students
        if name
    ]

    # Check that students were entered
    if not students:

        st.warning("Please enter at least one student name.")
        st.session_state.groups = None

    # Check that there are enough students
    elif num_groups > len(students):

        st.warning(
            f"You have {len(students)} students, so you cannot "
            f"create {num_groups} non-empty groups."
        )

        st.session_state.groups = None

    else:

        st.session_state.groups = create_groups(
            students,
            int(num_groups)
        )


# ---------------------------------------------------------
# Display groups
# ---------------------------------------------------------

if st.session_state.groups:

    st.subheader("Your Groups")

    groups = st.session_state.groups
    number_of_groups = len(groups)

    # Split groups into two rows
    midpoint = (number_of_groups + 1) // 2

    first_row = groups[:midpoint]
    second_row = groups[midpoint:]


    # -----------------------------------------------------
    # First row
    # -----------------------------------------------------

    columns = st.columns(len(first_row))

    for index, group in enumerate(first_row):

        with columns[index]:

            st.markdown(
                f'<div class="group-container">'
                f'<div class="group-title">'
                f'Group {index + 1}'
                f'</div>',
                unsafe_allow_html=True
            )

            for student in group:

                st.markdown(
                    f'<div class="student-name">'
                    f'• {student}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            st.markdown(
                f'<div class="student-count">'
                f'{len(group)} student'
                f'{"s" if len(group) != 1 else ""}'
                f'</div></div>',
                unsafe_allow_html=True
            )


    # -----------------------------------------------------
    # Second row
    # -----------------------------------------------------

    if second_row:

        st.markdown("---")

        columns = st.columns(len(second_row))

        for index, group in enumerate(second_row):

            group_number = midpoint + index + 1

            with columns[index]:

                st.markdown(
                    f'<div class="group-container">'
                    f'<div class="group-title">'
                    f'Group {group_number}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                for student in group:

                    st.markdown(
                        f'<div class="student-name">'
                        f'• {student}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f'<div class="student-count">'
                    f'{len(group)} student'
                    f'{"s" if len(group) != 1 else ""}'
                    f'</div></div>',
                    unsafe_allow_html=True
                )
