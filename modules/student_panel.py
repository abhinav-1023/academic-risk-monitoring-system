import streamlit as st
import pandas as pd

from utils.database import supabase

from modules.prediction import predict_risk

# -----------------------------------
# STUDENT DASHBOARD
# -----------------------------------

def student_dashboard():

    st.header("Student Dashboard")

    username = st.session_state.username

    # -----------------------------------
    # GET USER
    # -----------------------------------

    user_response = supabase.table(
        "users"
    ).select("*").eq(
        "username",
        username
    ).execute()

    user_data = user_response.data

    if not user_data:

        st.warning("User not found")

        return

    user_id = user_data[0]["id"]

    # -----------------------------------
    # GET STUDENT
    # -----------------------------------

    student_response = supabase.table(
        "students"
    ).select("*").eq(
        "user_id",
        user_id
    ).execute()

    student_data = student_response.data

    if not student_data:

        st.warning("Student record not found")

        return

    student = student_data[0]

    student_id = student["id"]

    student_name = student["student_name"]

    semester = student["semester"]

    # -----------------------------------
    # STUDENT DETAILS
    # -----------------------------------

    st.subheader("Student Information")

    st.write("Name:", student_name)

    st.write("Semester:", semester)

    st.write("---")

    # -----------------------------------
    # FETCH MARKS
    # -----------------------------------

    marks_response = supabase.table(
        "marks"
    ).select("*").eq(
        "student_id",
        student_id
    ).execute()

    marks_data = marks_response.data

    if not marks_data:

        st.info("No marks available yet")

        return

    # -----------------------------------
    # PERFORMANCE TABLE
    # -----------------------------------

    performance_data = []

    for mark in marks_data:

        subject_id = mark["subject_id"]

        # GET SUBJECT NAME

        subject_response = supabase.table(
            "subjects"
        ).select("*").eq(
            "id",
            subject_id
        ).execute()

        subject_data = subject_response.data

        subject_name = "Unknown"

        if subject_data:

            subject_name = subject_data[0]["subject_name"]

        attendance = mark["attendance"]

        internal = mark["internal_marks"]

        participation = mark["participation"]

        assignment = mark["assignment_score"]

        quiz = mark["quiz_score"]

        midsem = mark["midsem_marks"]

        risk = predict_risk(

            attendance,

            internal,

            participation,

            assignment,

            quiz,

            midsem
        )

        performance_data.append({

            "Subject": subject_name,

            "Attendance": attendance,

            "Internal": internal,

            "Participation": participation,

            "Assignment": assignment,

            "Quiz": quiz,

            "Midsem": midsem,

            "Risk": risk
        })

    # -----------------------------------
    # DISPLAY TABLE
    # -----------------------------------

    df = pd.DataFrame(performance_data)

    st.subheader("Academic Performance")

    st.dataframe(
        df,
        use_container_width=True
    )

    # -----------------------------------
    # RISK ANALYSIS
    # -----------------------------------

    st.subheader("Risk Analysis")

    for row in performance_data:

        subject = row["Subject"]

        risk = row["Risk"]

        st.write(f"Subject: {subject}")

        if risk == "High":

            st.error(
                "High Academic Risk"
            )

        elif risk == "Medium":

            st.warning(
                "Medium Academic Risk"
            )

        else:

            st.success(
                "Low Academic Risk"
            )

        # -----------------------------------
        # SUGGESTIONS
        # -----------------------------------

        st.write("Suggestions:")

        if row["Attendance"] < 70:

            st.write(
                "- Improve attendance"
            )

        if row["Internal"] < 15:

            st.write(
                "- Focus on internal preparation"
            )

        if row["Participation"] < 4:

            st.write(
                "- Participate more in classroom activities"
            )

        if row["Assignment"] < 12:

            st.write(
                "- Submit assignments properly"
            )

        if row["Quiz"] < 10:

            st.write(
                "- Improve quiz performance"
            )

        if row["Midsem"] < 20:

            st.write(
                "- Prepare better for mid-sem exams"
            )

        st.write("---")

    # -----------------------------------
    # VISUALIZATION
    # -----------------------------------

    st.subheader("Performance Visualization")

    chart_df = df[[
        "Attendance",
        "Internal",
        "Assignment",
        "Quiz",
        "Midsem"
    ]]

    st.bar_chart(chart_df)