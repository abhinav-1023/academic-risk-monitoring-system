import streamlit as st
import pandas as pd

from utils.database import supabase
from modules.prediction import predict_risk


def teacher_dashboard():

    st.header("AI Academic Risk Monitoring System")

    st.subheader("Teacher Dashboard")

    # -----------------------------------
    # GET SUBJECTS
    # -----------------------------------

    response = supabase.table(
        "subjects"
    ).select("*").execute()

    subjects = response.data

    if not subjects:

        st.warning("No subjects found")
        return

    subject_dict = {

        s["subject_name"]:
        (
            s["id"],
            s["semester"]
        )

        for s in subjects
    }

    # -----------------------------------
    # SUBJECT SELECTION
    # -----------------------------------

    col1, col2 = st.columns([3, 1])

    with col1:

        subject_name = st.selectbox(

            "Select Subject",

            list(subject_dict.keys())
        )

    subject_id, semester = subject_dict[
        subject_name
    ]

    with col2:

        st.metric(
            "Semester",
            semester
        )

    st.markdown("---")

    # -----------------------------------
    # GET STUDENTS
    # -----------------------------------

    response = supabase.table(
        "students"
    ).select("*").eq(
        "semester",
        semester
    ).execute()

    students = response.data

    if not students:

        st.warning("No students found")
        return

    student_names = [

        s["student_name"]

        for s in students
    ]

    # -----------------------------------
    # DATA ENTRY TABLE
    # -----------------------------------

    st.subheader(
        "Student Marks Entry"
    )

    df = pd.DataFrame({

        "Student":
            student_names,

        "Attendance":
            [75] * len(student_names),

        "Internal":
            [15] * len(student_names),

        "Participation":
            [5] * len(student_names),

        "Assignment":
            [15] * len(student_names),

        "Quiz":
            [10] * len(student_names),

        "Midsem":
            [20] * len(student_names)
    })

    edited_df = st.data_editor(

        df,

        use_container_width=True,

        hide_index=True
    )

    # -----------------------------------
    # BUTTONS
    # -----------------------------------

    col1, col2 = st.columns(2)

    # -----------------------------------
    # SAVE MARKS
    # -----------------------------------

    with col1:

        if st.button(
            "💾 Save Marks",
            use_container_width=True
        ):

            for i, row in edited_df.iterrows():

                student_id = students[i]["id"]

                attendance = row["Attendance"]

                internal = row["Internal"]

                participation = row["Participation"]

                assignment = row["Assignment"]

                quiz = row["Quiz"]

                midsem = row["Midsem"]

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

                # -----------------------------------
                # CHECK EXISTING RECORD
                # -----------------------------------

                existing = supabase.table(
                    "marks"
                ).select("*").eq(
                    "student_id",
                    student_id
                ).eq(
                    "subject_id",
                    subject_id
                ).execute()

                # -----------------------------------
                # UPDATE OR INSERT
                # -----------------------------------

                if existing.data:

                    record_id = existing.data[0]["id"]

                    supabase.table(
                        "marks"
                    ).update({

                        "attendance":
                            attendance,

                        "internal_marks":
                            internal,

                        "participation":
                            participation,

                        "assignment_score":
                            assignment,

                        "quiz_score":
                            quiz,

                        "midsem_marks":
                            midsem,

                        "risk_level":
                            risk

                    }).eq(
                        "id",
                        record_id
                    ).execute()

                else:

                    supabase.table(
                        "marks"
                    ).insert({

                        "student_id":
                            student_id,

                        "subject_id":
                            subject_id,

                        "attendance":
                            attendance,

                        "internal_marks":
                            internal,

                        "participation":
                            participation,

                        "assignment_score":
                            assignment,

                        "quiz_score":
                            quiz,

                        "midsem_marks":
                            midsem,

                        "risk_level":
                            risk

                    }).execute()

            st.success(
                "Marks Saved Successfully"
            )

    # -----------------------------------
    # GENERATE REPORT
    # -----------------------------------

    with col2:

        generate = st.button(

            "📊 Generate Risk Report",

            use_container_width=True
        )

    # -----------------------------------
    # REPORT
    # -----------------------------------

    if generate:

        st.markdown("---")

        st.subheader(
            "Student Risk Report"
        )

        marks_response = supabase.table(
            "marks"
        ).select("*").eq(
            "subject_id",
            subject_id
        ).execute()

        marks_data = marks_response.data

        if not marks_data:

            st.warning("No data found")
            return

        chart_students = []

        chart_internal = []

        chart_attendance = []

        chart_quiz = []

        # -----------------------------------
        # RISK CARDS
        # -----------------------------------

        cols = st.columns(2)

        for idx, data in enumerate(marks_data):

            student_id = data["student_id"]

            student_name = ""

            for s in students:

                if s["id"] == student_id:

                    student_name = s[
                        "student_name"
                    ]

            risk = data["risk_level"]

            with cols[idx % 2]:

                if risk == "High":

                    st.error(
                        f"🔴 {student_name} → HIGH RISK"
                    )

                elif risk == "Medium":

                    st.warning(
                        f"🟠 {student_name} → MEDIUM RISK"
                    )

                else:

                    st.success(
                        f"🟢 {student_name} → LOW RISK"
                    )

            chart_students.append(
                student_name
            )

            chart_internal.append(
                data["internal_marks"]
            )

            chart_attendance.append(
                data["attendance"]
            )

            chart_quiz.append(
                data["quiz_score"]
            )

        st.markdown("---")

        # -----------------------------------
        # PERFORMANCE ANALYTICS
        # -----------------------------------

        st.subheader(
            "Performance Analytics"
        )

        col1, col2 = st.columns(2)

        # -----------------------------------
        # INTERNAL MARKS
        # -----------------------------------

        with col1:

            internal_df = pd.DataFrame({

                "Students":
                    chart_students,

                "Internal":
                    chart_internal
            })

            st.markdown(
                "### Internal Marks"
            )

            st.bar_chart(

                internal_df.set_index(
                    "Students"
                ),

                height=250
            )

        # -----------------------------------
        # ATTENDANCE
        # -----------------------------------

        with col2:

            attendance_df = pd.DataFrame({

                "Students":
                    chart_students,

                "Attendance":
                    chart_attendance
            })

            st.markdown(
                "### Attendance"
            )

            st.line_chart(

                attendance_df.set_index(
                    "Students"
                ),

                height=250
            )

        st.markdown("")

        # -----------------------------------
        # QUIZ PERFORMANCE
        # -----------------------------------

        quiz_df = pd.DataFrame({

            "Students":
                chart_students,

            "Quiz":
                chart_quiz
        })

        st.markdown(
            "### Quiz Performance"
        )

        st.area_chart(

            quiz_df.set_index(
                "Students"
            ),

            height=220
        )