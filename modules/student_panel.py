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
    # PERFORMANCE DATA
    # -----------------------------------

    performance_data = []

    for mark in marks_data:

        subject_id = mark["subject_id"]

        # -----------------------------------
        # GET SUBJECT NAME
        # -----------------------------------

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

        # -----------------------------------
        # PREDICT RISK
        # -----------------------------------

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
    # PERFORMANCE VISUALIZATION
    # -----------------------------------

    st.subheader("Performance Visualization")

    for row in performance_data:

        st.markdown(
            f"### {row['Subject']}"
        )

        # Attendance

        st.write("Attendance")

        st.progress(
            int(row["Attendance"])
        )

        # Internal Marks

        st.write("Internal Marks")

        st.progress(
            min(int(row["Internal"] * 4), 100)
        )

        # Assignment Score

        st.write("Assignment Score")

        st.progress(
            min(int(row["Assignment"] * 4), 100)
        )

        # Quiz Score

        st.write("Quiz Score")

        st.progress(
            min(int(row["Quiz"] * 5), 100)
        )

        # Midsem Marks

        st.write("Midsem Marks")

        st.progress(
            min(int(row["Midsem"] * 2.5), 100)
        )

        st.write("---")

    # -----------------------------------
    # RADAR STYLE ANALYTICS
    # -----------------------------------

    st.subheader("Performance Analytics")

    col1, col2 = st.columns(2)

    # -----------------------------------
    # LEFT ANALYTICS
    # -----------------------------------

    with col1:

        st.markdown("#### Academic Metrics")

        academic_df = pd.DataFrame({

            "Metrics": [

                "Attendance",

                "Internal",

                "Assignment",

                "Midsem"
            ],

            "Scores": [

                df["Attendance"].mean(),

                df["Internal"].mean() * 4,

                df["Assignment"].mean() * 4,

                df["Midsem"].mean() * 2.5
            ]
        })

        st.line_chart(
            academic_df.set_index("Metrics"),
            height=250
        )

    # -----------------------------------
    # RIGHT ANALYTICS
    # -----------------------------------

    with col2:

        st.markdown("#### Engagement Metrics")

        engagement_df = pd.DataFrame({

            "Metrics": [

                "Participation",

                "Quiz"
            ],

            "Scores": [

                df["Participation"].mean() * 10,

                df["Quiz"].mean() * 5
            ]
        })

        st.line_chart(
            engagement_df.set_index("Metrics"),
            height=250
        )