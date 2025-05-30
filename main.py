import streamlit as st
import pandas as pd 

st.set_page_config(
    page_title="Ponteng Hour Calculator",
    page_icon=":calculator:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize ALL state variables at the very beginning
if 'num_rows' not in st.session_state:
    st.session_state.num_rows = 6

# No need for calculate_clicked state anymore
# We'll create callback functions to update calculations
def update_input():
    # This function will be called whenever any input changes
    # It doesn't need to do anything since the app will rerun automatically
    pass

st.markdown("# _Ponteng_ Calculator")
st.markdown("Made by [tzhenyu](https://github.com/tzhenyu)")
st.markdown("Calcuate your minimum attendance hour for each course!")
st.markdown("Write down your course name, lecture hours, tutorial hours and practical hours in a week.")
st.markdown("You can check the ponteng hour at the bottom of the page.")
# Add enhanced CSS for mobile responsiveness
st.markdown("""
<style>
    @media screen and (max-width: 768px) {
        /* Force buttons to be full width on mobile */
        .stButton button {
            width: 100% !important;
        }
        
        /* Show mobile headers */
        .mobile-header {
            display: block !important;
            font-weight: bold;
            margin: 5px 0;
        }
    }
    
    /* By default hide mobile headers */
    .mobile-header {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

option = st.selectbox(
     'Weeks in Semester',
     ('Short Semester (7 weeks)', 'Long Semester (14 weeks)'),
     on_change=update_input)

# Create input rows with mobile-friendly styling
for i in range(st.session_state.num_rows):
    st.markdown('<hr style="margin: 10px 0;">', unsafe_allow_html=True)

    cols = st.columns([2, 1, 1, 1], gap="small")
    
    with cols[0]:
        st.text_input(f"Course {i+1} Name", key=f"row{i}_col1", on_change=update_input)
        
    with cols[1]:
        st.number_input("Lecture Hours in a week", key=f"row{i}_col2", step=0.5, 
                         min_value=0.0, format="%.1f", on_change=update_input)
        
    with cols[2]:
        st.number_input("Tutorial Hours in a week", key=f"row{i}_col3", step=0.5, 
                         min_value=0.0, format="%.1f", on_change=update_input)
        
    with cols[3]:
        st.number_input("Practical Hours in a week", key=f"row{i}_col4", step=0.5, 
                         min_value=0.0, format="%.1f", on_change=update_input)

# Now calculate and display results automatically
st.markdown('<hr style="margin: 20px 0;">', unsafe_allow_html=True)
st.subheader("Calculation Results")

# Calculate results
weeks = 7 if option == 'Short Semester (7 weeks)' else 14

# Display the calculation results in a table
data = []
total_hours = 0

for i in range(st.session_state.num_rows):
    # Get form input values from session state
    course_name = st.session_state.get(f"row{i}_col1", "")
    lecture_hours = st.session_state.get(f"row{i}_col2", 0.0)
    tutorial_hours = st.session_state.get(f"row{i}_col3", 0.0)
    practical_hours = st.session_state.get(f"row{i}_col4", 0.0)
    
    # Skip empty rows
    if not course_name:
        continue
        
    # Calculate total weekly hours
    weekly_hours = lecture_hours + tutorial_hours + practical_hours
    
    # Calculate total semester hours
    semester_hours = weekly_hours * weeks
    
    # Calculate minimum attendance hours (80%)
    min_attendance = weekly_hours * (weeks-2) * 0.2
    
    # Add to total
    total_hours += min_attendance
    
    # Add to data for display
    data.append({
        "Course": course_name,
        # "Weekly Hours": f"{weekly_hours:.1f}",
        # "Semester Hours": f"{semester_hours:.1f}",
        "Ponteng Hour (Before barred list)": f"{min_attendance:.1f}"
    })

# Display results
if data:
    st.write("Make sure you don't lose your attendance hour more than this to prevent getting barred!")
    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=True)
    
else:
    st.warning("No course data entered. Please enter at least one course name.")

