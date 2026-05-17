import streamlit as st

from utils.database import supabase

# -----------------------------------
# ADMIN DASHBOARD
# -----------------------------------

def admin_dashboard():

    st.header("Academic Coordinator Dashboard")

    menu = st.sidebar.selectbox(

        "Coordinator Menu",

        [

            "Create Teacher",

            "Create Student",

            "Create Subject",

            "Assign Teacher to Subject"
        ]
    )

    # =================================================
    # CREATE TEACHER
    # =================================================

    if menu == "Create Teacher":

        st.subheader("Create Teacher")

        username = st.text_input(
            "Teacher Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        department = st.text_input(
            "Department"
        )

        if st.button("Create Teacher"):

            try:

                # -----------------------------------
                # INSERT USER
                # -----------------------------------

                user_response = supabase.table(
                    "users"
                ).insert({

                    "username": username,

                    "password": password,

                    "role": "Teacher",

                    "department": department

                }).execute()

                user_id = user_response.data[0]["id"]

                # -----------------------------------
                # INSERT TEACHER
                # -----------------------------------

                supabase.table(
                    "teachers"
                ).insert({

                    "user_id": user_id,

                    "department": department

                }).execute()

                st.success(
                    "Teacher created successfully"
                )

            except Exception as e:

                st.error(f"Error: {e}")

    # =================================================
    # CREATE STUDENT
    # =================================================

    elif menu == "Create Student":

        st.subheader("Create Student")

        student_name = st.text_input(
            "Student Full Name"
        )

        username = st.text_input(
            "Student Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        # ONLY 1st and 3rd semester

        semester = st.selectbox(

            "Current Semester",

            [1, 3]
        )

        if st.button("Create Student"):

            try:

                # -----------------------------------
                # INSERT USER
                # -----------------------------------

                user_response = supabase.table(
                    "users"
                ).insert({

                    "username": username,

                    "password": password,

                    "role": "Student",

                    "department": "CSE"

                }).execute()

                user_id = user_response.data[0]["id"]

                # -----------------------------------
                # INSERT STUDENT
                # -----------------------------------

                supabase.table(
                    "students"
                ).insert({

                    "user_id": user_id,

                    "student_name": student_name,

                    "semester": semester

                }).execute()

                st.success(

                    f"Student '{student_name}' created successfully"
                )

            except Exception as e:

                st.error(f"Error: {e}")

    # =================================================
    # CREATE SUBJECT
    # =================================================

    elif menu == "Create Subject":

        st.subheader("Create Subject")

        subject_name = st.text_input(
            "Subject Name"
        )

        semester = st.selectbox(

            "Semester",

            [1, 3]
        )

        if st.button("Create Subject"):

            try:

                supabase.table(
                    "subjects"
                ).insert({

                    "subject_name": subject_name,

                    "semester": semester

                }).execute()

                st.success(
                    "Subject created successfully"
                )

            except Exception as e:

                st.error(f"Error: {e}")

    # =================================================
    # ASSIGN TEACHER TO SUBJECT
    # =================================================

    elif menu == "Assign Teacher to Subject":

        st.subheader("Assign Teacher")

        # -----------------------------------
        # FETCH SUBJECTS
        # -----------------------------------

        subjects_response = supabase.table(
            "subjects"
        ).select("*").execute()

        subjects = subjects_response.data

        if not subjects:

            st.warning(
                "No subjects available"
            )

            return

        subject_dict = {

            s["subject_name"]: s["id"]

            for s in subjects
        }

        subject_name = st.selectbox(

            "Select Subject",

            list(subject_dict.keys())
        )

        subject_id = subject_dict[subject_name]

        # -----------------------------------
        # FETCH TEACHERS
        # -----------------------------------

        teachers_response = supabase.table(
            "teachers"
        ).select("*").execute()

        teachers = teachers_response.data

        if not teachers:

            st.warning(
                "No teachers available"
            )

            return

        teacher_names = []

        teacher_map = {}

        for teacher in teachers:

            user_id = teacher["user_id"]

            user_response = supabase.table(
                "users"
            ).select("*").eq(
                "id",
                user_id
            ).execute()

            user_data = user_response.data

            if user_data:

                username = user_data[0]["username"]

                teacher_names.append(username)

                teacher_map[username] = teacher["id"]

        teacher_name = st.selectbox(

            "Select Teacher",

            teacher_names
        )

        teacher_id = teacher_map[teacher_name]

        # -----------------------------------
        # ASSIGN BUTTON
        # -----------------------------------

        if st.button("Assign Teacher"):

            try:

                supabase.table(
                    "subjects"
                ).update({

                    "teacher_id": teacher_id

                }).eq(

                    "id",
                    subject_id

                ).execute()

                st.success(

                    f"{teacher_name} assigned to {subject_name}"
                )

            except Exception as e:

                st.error(f"Error: {e}")