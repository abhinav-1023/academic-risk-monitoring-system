import streamlit as st
import sqlite3
import os

from modules.prediction import predict_risk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "..", "database", "college_system.db")


def get_connection():
    return sqlite3.connect(db_path)


def student_dashboard():

    st.header("Student Dashboard")

    username = st.session_state.username

    conn = get_connection()
    cursor = conn.cursor()

    
    # GET STUDENT INFORMATION
    

    cursor.execute("""
    SELECT students.id, students.previous_gpa
    FROM students
    JOIN users ON students.user_id = users.id
    WHERE users.username=?
    """, (username,))

    student = cursor.fetchone()

    if not student:
        st.warning("Student record not found")
        return

    student_id, gpa = student

    
    # GET MARKS
    

    cursor.execute("""
    SELECT subjects.subject_name,
           marks.attendance,
           marks.internal_marks,
           marks.participation,
           marks.absences
    FROM marks
    JOIN subjects ON marks.subject_id = subjects.id
    WHERE marks.student_id=?
    """, (student_id,))

    records = cursor.fetchall()

    if not records:
        st.info("No marks available yet")
        return

    
    # DISPLAY SUBJECT PERFORMANCE
    

    for subject_name, attendance, internal, participation, absences in records:

        st.subheader(subject_name)

        st.write("Attendance:", attendance, "%")
        st.write("Internal Marks:", internal)
        st.write("Participation:", participation)
        st.write("Absences:", absences)

        # Predict risk
        risk = predict_risk(
            attendance,
            internal,
            participation,
            absences,
            gpa
        )

        # Show risk level
        if risk == "High":
            st.error("Risk Level: High Risk")

        elif risk == "Medium":
            st.warning("Risk Level: Medium Risk")

        else:
            st.success("Risk Level: Low Risk")

        
        # Suggestions
        

        st.write("Suggestions:")

        if attendance < 70:
            st.write("- Improve class attendance")

        if internal < 15:
            st.write("- Work harder for internal assessments")

        if participation < 4:
            st.write("- Participate more in class")

        if absences > 5:
            st.write("- Reduce number of absences")

        st.write("---")