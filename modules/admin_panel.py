import streamlit as st

from utils.database import supabase


def admin_dashboard():

    st.header("AI Academic Risk Monitoring System")

    st.subheader("Academic Coordinator Dashboard")

    # -----------------------------------
    # SIDEBAR MENU
    # -----------------------------------

    menu = st.sidebar.radio(

        "Coordinator Menu",

        [

            "Create Teacher",

            "Create Student",

            "Create Subject",

            "Assign Teacher"
        ]
    )

    # ===================================
    # CREATE TEACHER
    # ===================================

    if menu == "Create Teacher":

        st.markdown(
            "## 👨‍🏫 Create Teacher"
        )

        col1, col2 = st.columns(2)

        with col1:

            username = st.text_input(
                "Teacher Username"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

        with col2:

            department = st.selectbox(

                "Department",

                [

                    "CSE",

                    "ECE",

                    "ME",

                    "CE",

                    "EE"
                ]
            )

            email = st.text_input(
                "Email"
            )

        st.markdown("")

        if st.button(

            "➕ Create Teacher",

            use_container_width=True
        ):

            # -----------------------------------
            # INSERT INTO USERS
            # -----------------------------------

            user_response = supabase.table(
                "users"
            ).insert({

                "username":
                    username,

                "password":
                    password,

                "role":
                    "Teacher"

            }).execute()

            user_id = user_response.data[0]["id"]

            # -----------------------------------
            # INSERT INTO TEACHERS
            # -----------------------------------

            supabase.table(
                "teachers"
            ).insert({

                "user_id":
                    user_id,

                "teacher_name":
                    username,

                "department":
                    department,

                "email":
                    email

            }).execute()

            st.success(
                "Teacher Created Successfully"
            )

    # ===================================
    # CREATE STUDENT
    # ===================================

    elif menu == "Create Student":

        st.markdown(
            "## 👨‍🎓 Create Student"
        )

        col1, col2 = st.columns(2)

        with col1:

            username = st.text_input(
                "Student Username"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

        with col2:

            semester = st.selectbox(

                "Semester",

                [1, 2, 3, 4, 5, 6, 7, 8]
            )

            department = st.selectbox(

                "Department",

                [

                    "CSE",

                    "ECE",

                    "ME",

                    "CE",

                    "EE"
                ]
            )

        st.markdown("")

        if st.button(

            "➕ Create Student",

            use_container_width=True
        ):

            # -----------------------------------
            # INSERT USER
            # -----------------------------------

            user_response = supabase.table(
                "users"
            ).insert({

                "username":
                    username,

                "password":
                    password,

                "role":
                    "Student"

            }).execute()

            user_id = user_response.data[0]["id"]

            # -----------------------------------
            # INSERT STUDENT
            # -----------------------------------

            supabase.table(
                "students"
            ).insert({

                "user_id":
                    user_id,

                "student_name":
                    username,

                "semester":
                    semester,

                "department":
                    department

            }).execute()

            st.success(
                "Student Created Successfully"
            )

    # ===================================
    # CREATE SUBJECT
    # ===================================

    elif menu == "Create Subject":

        st.markdown(
            "## 📚 Create Subject"
        )

        col1, col2 = st.columns(2)

        with col1:

            subject_name = st.text_input(
                "Subject Name"
            )

        with col2:

            semester = st.selectbox(

                "Semester",

                [1, 2, 3, 4, 5, 6, 7, 8]
            )

        st.markdown("")

        if st.button(

            "➕ Create Subject",

            use_container_width=True
        ):

            supabase.table(
                "subjects"
            ).insert({

                "subject_name":
                    subject_name,

                "semester":
                    semester

            }).execute()

            st.success(
                "Subject Created Successfully"
            )

    # ===================================
    # ASSIGN TEACHER
    # ===================================

    elif menu == "Assign Teacher":

        st.markdown(
            "## 🔗 Assign Teacher To Subject"
        )

        # -----------------------------------
        # GET SUBJECTS
        # -----------------------------------

        subject_response = supabase.table(
            "subjects"
        ).select("*").execute()

        subjects = subject_response.data

        subject_dict = {

            s["subject_name"]:
                s["id"]

            for s in subjects
        }

        # -----------------------------------
        # GET TEACHERS
        # -----------------------------------

        teacher_response = supabase.table(
            "teachers"
        ).select("*").execute()

        teachers = teacher_response.data

        teacher_dict = {

            t["teacher_name"]:
                t["id"]

            for t in teachers
        }

        col1, col2 = st.columns(2)

        with col1:

            selected_subject = st.selectbox(

                "Select Subject",

                list(subject_dict.keys())
            )

        with col2:

            selected_teacher = st.selectbox(

                "Select Teacher",

                list(teacher_dict.keys())
            )

        st.markdown("")

        if st.button(

            "✅ Assign Teacher",

            use_container_width=True
        ):

            supabase.table(
                "subjects"
            ).update({

                "teacher_id":
                    teacher_dict[
                        selected_teacher
                    ]

            }).eq(

                "id",

                subject_dict[
                    selected_subject
                ]

            ).execute()

            st.success(

                f"{selected_teacher} assigned to {selected_subject}"
            )

    # ===================================
    # DASHBOARD SUMMARY
    # ===================================

    st.markdown("---")

    st.subheader("System Overview")

    col1, col2, col3 = st.columns(3)

    # -----------------------------------
    # TOTAL STUDENTS
    # -----------------------------------

    students = supabase.table(
        "students"
    ).select("*").execute()

    with col1:

        st.metric(

            "Students",

            len(students.data)
        )

    # -----------------------------------
    # TOTAL TEACHERS
    # -----------------------------------

    teachers = supabase.table(
        "teachers"
    ).select("*").execute()

    with col2:

        st.metric(

            "Teachers",

            len(teachers.data)
        )

    # -----------------------------------
    # TOTAL SUBJECTS
    # -----------------------------------

    subjects = supabase.table(
        "subjects"
    ).select("*").execute()

    with col3:

        st.metric(

            "Subjects",

            len(subjects.data)
        )