import streamlit as st
import pandas as pd

from utils.database import supabase


def student_dashboard():

    st.header("AI Academic Risk Monitoring System")

    username = st.session_state.username

    # -----------------------------------
    # GET STUDENT INFO
    # -----------------------------------

    response = supabase.table(
        "students"
    ).select("*").eq(
        "student_name",
        username
    ).execute()

    students = response.data

    if not students:

        st.error("Student not found")
        return

    student = students[0]

    student_id = student["id"]

    semester = student["semester"]

    # -----------------------------------
    # STUDENT INFO
    # -----------------------------------

    st.subheader("Student Dashboard")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            ### 👤 Student Information

            **Name:** {username}

            **Semester:** {semester}
            """
        )

    with col2:

        st.info(
            "Track your academic performance and risk level in real time."
        )

    st.markdown("---")

    # -----------------------------------
    # GET MARKS
    # -----------------------------------

    marks_response = supabase.table(
        "marks"
    ).select("*").eq(
        "student_id",
        student_id
    ).execute()

    marks_data = marks_response.data

    if not marks_data:

        st.warning("No academic data available")
        return

    # -----------------------------------
    # GET SUBJECT NAMES
    # -----------------------------------

    subjects_response = supabase.table(
        "subjects"
    ).select("*").execute()

    subjects = subjects_response.data

    subject_map = {}

    for sub in subjects:

        subject_map[sub["id"]] = sub["subject_name"]

    # -----------------------------------
    # PERFORMANCE TABLE
    # -----------------------------------

    performance_data = []

    for row in marks_data:

        performance_data.append({

            "Subject":
                subject_map.get(
                    row["subject_id"],
                    "Unknown"
                ),

            "Attendance":
                row["attendance"],

            "Internal":
                row["internal_marks"],

            "Participation":
                row["participation"],

            "Assignment":
                row["assignment_score"],

            "Quiz":
                row["quiz_score"],

            "Midsem":
                row["midsem_marks"],

            "Risk":
                row["risk_level"]
        })

    df = pd.DataFrame(performance_data)

    # -----------------------------------
    # ACADEMIC PERFORMANCE
    # -----------------------------------

    st.subheader("Academic Performance")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.markdown("---")

    # -----------------------------------
    # RISK ANALYSIS
    # -----------------------------------

    st.subheader("Risk Analysis")

    for row in performance_data:

        st.markdown(
            f"### 📘 {row['Subject']}"
        )

        risk = row["Risk"]

        if risk == "High":

            st.error(
                "🔴 High Academic Risk"
            )

        elif risk == "Medium":

            st.warning(
                "🟠 Medium Academic Risk"
            )

        else:

            st.success(
                "🟢 Low Academic Risk"
            )

        # -----------------------------------
        # SUGGESTIONS
        # -----------------------------------

        suggestions = []

        if row["Attendance"] < 70:

            suggestions.append(
                "Improve attendance"
            )

        if row["Internal"] < 15:

            suggestions.append(
                "Focus on internal preparation"
            )

        if row["Participation"] < 4:

            suggestions.append(
                "Participate more in classroom activities"
            )

        if row["Assignment"] < 10:

            suggestions.append(
                "Submit assignments properly"
            )

        if row["Quiz"] < 8:

            suggestions.append(
                "Improve quiz performance"
            )

        if row["Midsem"] < 18:

            suggestions.append(
                "Prepare better for mid-sem exams"
            )

        st.markdown("#### Suggestions")

        if len(suggestions) == 0:

            st.success(
                "✅ No suggestions needed. Performance is good."
            )

        else:

            for item in suggestions:

                st.write(f"• {item}")

        st.markdown("---")

    # -----------------------------------
    # PERFORMANCE VISUALIZATION
    # -----------------------------------

    st.subheader("Performance Visualization")

    for row in performance_data:

        st.markdown(
            f"### 📘 {row['Subject']}"
        )

        col1, col2 = st.columns(2)

        # -----------------------------------
        # LEFT SIDE
        # -----------------------------------

        with col1:

            st.caption("Attendance")

            st.progress(
                int(row["Attendance"])
            )

            st.caption("Internal")

            st.progress(
                min(int(row["Internal"] * 4), 100)
            )

            st.caption("Assignment")

            st.progress(
                min(int(row["Assignment"] * 4), 100)
            )

        # -----------------------------------
        # RIGHT SIDE
        # -----------------------------------

        with col2:

            st.caption("Quiz")

            st.progress(
                min(int(row["Quiz"] * 5), 100)
            )

            st.caption("Midsem")

            st.progress(
                min(int(row["Midsem"] * 2.5), 100)
            )

            st.caption("Participation")

            st.progress(
                min(int(row["Participation"] * 10), 100)
            )

        st.markdown("---")

    # -----------------------------------
    # PERFORMANCE ANALYTICS
    # -----------------------------------

    st.subheader("Performance Analytics")

    col1, col2 = st.columns(2)

    # -----------------------------------
    # ACADEMIC METRICS
    # -----------------------------------

    with col1:

        st.markdown(
            "### Academic Metrics"
        )

        academic_df = pd.DataFrame({

            "Metrics": [

                "Assignment",

                "Attendance",

                "Internal",

                "Midsem"
            ],

            "Scores": [

                df["Assignment"].mean() * 4,

                df["Attendance"].mean(),

                df["Internal"].mean() * 4,

                df["Midsem"].mean() * 2.5
            ]
        })

        st.area_chart(

            academic_df.set_index(
                "Metrics"
            ),

            height=220
        )

    # -----------------------------------
    # ENGAGEMENT METRICS
    # -----------------------------------

    with col2:

        st.markdown(
            "### Engagement Metrics"
        )

        engagement_df = pd.DataFrame({

            "Metrics": [

                "Participation",

                "Quiz",

                "Attendance"
            ],

            "Scores": [

                df["Participation"].mean() * 10,

                df["Quiz"].mean() * 5,

                df["Attendance"].mean()
            ]
        })

        st.area_chart(

            engagement_df.set_index(
                "Metrics"
            ),

            height=220
        )