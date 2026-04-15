import streamlit as st
import sqlite3
import pandas as pd
import os

from modules.prediction import predict_risk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "..", "database", "college_system.db")


def get_connection():
    return sqlite3.connect(db_path)


def teacher_dashboard():

    st.header("Teacher Dashboard")

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------------
    # GET SUBJECTS
    # -----------------------------------

    cursor.execute("SELECT id, subject_name, semester FROM subjects")
    subjects = cursor.fetchall()

    if not subjects:
        st.warning("No subjects found")
        return

    subject_dict = {s[1]: (s[0], s[2]) for s in subjects}

    subject_name = st.selectbox("Select Subject", list(subject_dict.keys()))

    subject_id, semester = subject_dict[subject_name]

    st.write("Semester:", semester)

    # -----------------------------------
    # GET STUDENTS
    # -----------------------------------

    cursor.execute("""
    SELECT students.id, users.username, students.previous_gpa
    FROM students
    JOIN users ON students.user_id = users.id
    WHERE students.semester=?
    """, (semester,))

    students = cursor.fetchall()

    if not students:
        st.warning("No students found for this semester")
        return

    student_names = [s[1] for s in students]

    # -----------------------------------
    # MARK ENTRY TABLE
    # -----------------------------------

    df = pd.DataFrame({
        "Student": student_names,
        "Attendance": [75]*len(student_names),
        "Internal": [15]*len(student_names),
        "Participation": [5]*len(student_names),
        "Absences": [0]*len(student_names)
    })

    edited_df = st.data_editor(df)

    # -----------------------------------
    # SAVE MARKS
    # -----------------------------------

    if st.button("Save Marks"):

        for i, row in edited_df.iterrows():

            student_id = students[i][0]

            attendance = row["Attendance"]
            internal = row["Internal"]
            participation = row["Participation"]
            absences = row["Absences"]

            cursor.execute("""
            INSERT INTO marks
            (student_id, subject_id, attendance, internal_marks, participation, absences)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                subject_id,
                attendance,
                internal,
                participation,
                absences
            ))

        conn.commit()

        st.success("Marks saved successfully")

    # -----------------------------------
    # GENERATE RISK REPORT
    # -----------------------------------

    if st.button("Generate Risk Report"):

        st.subheader("Risk Prediction")

        for student_id, student_name, gpa in students:

            cursor.execute("""
            SELECT attendance, internal_marks, participation, absences
            FROM marks
            WHERE student_id=? AND subject_id=?
            ORDER BY id DESC LIMIT 1
            """, (student_id, subject_id))

            data = cursor.fetchone()

            if data:

                attendance, internal, participation, absences = data

                risk = predict_risk(
                    attendance,
                    internal,
                    participation,
                    absences,
                    gpa
                )

                if risk == "High":
                    st.error(f"{student_name} → {risk} Risk")

                elif risk == "Medium":
                    st.warning(f"{student_name} → {risk} Risk")

                else:
                    st.success(f"{student_name} → {risk} Risk")

                # -----------------------------------
                # SAVE DATA TO DATASET
                # -----------------------------------

                new_row = pd.DataFrame([{
                    "attendance": attendance,
                    "internal": internal,
                    "participation": participation,
                    "absences": absences,
                    "gpa": gpa,
                    "risk": risk
                }])

                dataset_path = "data/student_performance_dataset.csv"

                if os.path.exists(dataset_path):
                    new_row.to_csv(dataset_path, mode="a", header=False, index=False)
                else:
                    new_row.to_csv(dataset_path, index=False)