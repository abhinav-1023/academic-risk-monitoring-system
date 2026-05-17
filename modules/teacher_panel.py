import streamlit as st
import pandas as pd

from utils.database import supabase
from modules.prediction import predict_risk


def teacher_dashboard():

    st.header("Teacher Dashboard")

    
    # GET SUBJECTS
    

    response = supabase.table("subjects").select("*").execute()

    subjects = response.data

    if not subjects:
        st.warning("No subjects found")
        return

    subject_dict = {
        s["subject_name"]: (s["id"], s["semester"])
        for s in subjects
    }

    subject_name = st.selectbox(
        "Select Subject",
        list(subject_dict.keys())
    )

    subject_id, semester = subject_dict[subject_name]

    st.write("Semester:", semester)

    
    # GET STUDENTS
    

    response = supabase.table("students").select("*").eq(
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

    
    # DATA ENTRY TABLE
    

    df = pd.DataFrame({

        "Student": student_names,

        "Attendance": [75] * len(student_names),

        "Internal": [15] * len(student_names),

        "Participation": [5] * len(student_names),

        "Assignment": [15] * len(student_names),

        "Quiz": [10] * len(student_names),

        "Midsem": [20] * len(student_names)
    })

    edited_df = st.data_editor(
        df,
        use_container_width=True
    )

    
    # SAVE MARKS
    

    if st.button("Save Marks"):

        for i, row in edited_df.iterrows():

            student_id = students[i]["id"]

            attendance = row["Attendance"]

            internal = row["Internal"]

            participation = row["Participation"]

            assignment = row["Assignment"]

            quiz = row["Quiz"]

            midsem = row["Midsem"]

            
            # PREDICT RISK
            

            risk = predict_risk(
                attendance,
                internal,
                participation,
                assignment,
                quiz,
                midsem
            )

            
            # SAVE TO SUPABASE
            

            supabase.table("marks").insert({

                "student_id": student_id,

                "subject_id": subject_id,

                "attendance": attendance,

                "internal_marks": internal,

                "participation": participation,

                "assignment_score": assignment,

                "quiz_score": quiz,

                "midsem_marks": midsem,

                "risk_level": risk

            }).execute()

        st.success("Marks Saved Successfully")

    
    # GENERATE REPORT
    

    if st.button("Generate Risk Report"):

        st.subheader("Student Risk Report")

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
        chart_marks = []

        for data in marks_data:

            student_id = data["student_id"]

            student_name = ""

            for s in students:

                if s["id"] == student_id:
                    student_name = s["student_name"]

            risk = data["risk_level"]

            if risk == "High":

                st.error(
                    f"{student_name} → HIGH RISK"
                )

            elif risk == "Medium":

                st.warning(
                    f"{student_name} → MEDIUM RISK"
                )

            else:

                st.success(
                    f"{student_name} → LOW RISK"
                )

            chart_students.append(student_name)

            chart_marks.append(
                data["internal_marks"]
            )

        
        # BAR CHART
        

        chart_df = pd.DataFrame({

            "Students": chart_students,

            "Marks": chart_marks

        })

        st.subheader(
            "Student Performance Comparison"
        )

        st.bar_chart(
            chart_df.set_index("Students")
        )