import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Connection Setup
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("School Portal Navigation")
page = st.sidebar.radio("Go to:", ["Teacher: Grade Entry", "Admin: School Fees"])

# --- PAGE 1: TEACHER GRADE ENTRY ---
if page == "Teacher: Grade Entry":
    st.title("📝 Student Report Entry")
    
    with st.form("grade_form"):
        col1, col2 = st.columns(2)
        with col1:
            student_name = st.text_input("NAME")
            roll_no = st.number_input("NO. ON ROLL", step=1)
            term = st.selectbox("TERM", ["1st Term", "2nd Term", "3rd Term"])
        with col2:
            basic_class = st.selectbox("BASIC (CLASS)", ["Basic 1", "Basic 2", "Basic 3", "Basic 4", "Basic 5", "Basic 6", "Basic 7", "Basic 8", "Basic 9"])
            position = st.text_input("POSITION")
            vacation_date = st.date_input("VACATION DATE")
            reopening_date = st.date_input("REOPENING DATE")

        st.subheader("Academic Scores")
        subjects = ["ENGLISH", "RME", "SCIENCE", "MATHEMATICS", "COMPUTING", "FRENCH", "TWI", "CREATIVE ARTS", "CAREER TECH", "SOCIAL STUDIES"]
        
        score_data = {}
        for sub in subjects:
            cols = st.columns([2, 1, 1])
            cols[0].write(f"**{sub}**")
            c_score = cols[1].number_input("30%", min_value=0.0, max_value=30.0, key=f"{sub}_c")
            e_score = cols[2].number_input("70%", min_value=0.0, max_value=70.0, key=f"{sub}_e")
            score_data[sub] = c_score + e_score

        submit_grades = st.form_submit_button("Save Grades to Cloud")
        if submit_grades:
            # (Logic to save grades to Google Sheets goes here)
            st.success(f"Grades for {student_name} uploaded! ✅")

# --- PAGE 2: ADMIN SCHOOL FEES ---
elif page == "Admin: School Fees":
    st.title("💰 Finance & School Fees Management")
    
    # Simple Security Check
    admin_pin = st.text_input("Enter Admin PIN", type="password")
    
    if admin_pin == "1234": # You can change this to any PIN you like
        st.success("Access Granted")
        
        with st.form("fees_form"):
            target_student = st.text_input("Student Name for Fees")
            
            f1, f2 = st.columns(2)
            with f1:
                tuition = f1.number_input("Tuition Fees", value=0.0)
                pta = f1.number_input("P.T.A", value=0.0)
                building = f1.number_input("Building Maintenance", value=0.0)
            with f2:
                first_aid = f2.number_input("First Aid", value=0.0)
                materials = f2.number_input("Educational Materials", value=0.0)
                open_day = f2.number_input("Open Day Celebration", value=0.0)
                arrears = f2.number_input("Arrears", value=0.0)
            
            # AUTOMATIC CALCULATION
            total_fees = tuition + pta + building + first_aid + materials + open_day + arrears
            st.metric("TOTAL AMOUNT DUE", f"GHS {total_fees}")

            submit_fees = st.form_submit_button("Update Student Fees")
            if submit_fees:
                # (Logic to update the specific student's fees in Google Sheets)
                st.success(f"Fees updated for {target_student}!")
    
    elif admin_pin != "":
        st.error("Incorrect PIN. Access Denied.")
