import streamlit as st
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "..", "database", "college_system.db")


def get_connection():
    return sqlite3.connect(db_path)


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

    conn = get_connection()
    cursor = conn.cursor()

    # ------------------------------------------------
    # CREATE TEACHER
    # ------------------------------------------------

    if menu == "Create Teacher":

        st.subheader("Create Teacher")

        username = st.text_input("Teacher Username")
        password = st.text_input("Password", type="password")
        department = st.text_input("Department")

        if st.button("Create Teacher"):

            cursor.execute(
                """
                INSERT INTO users (username, password, role, department)
                VALUES (?, ?, 'Teacher', ?)
                """,
                (username, password, department)
            )

            user_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO teachers (user_id, department)
                VALUES (?, ?)
                """,
                (user_id, department)
            )

            conn.commit()

            st.success("Teacher created successfully")

    # ------------------------------------------------
    # CREATE STUDENT
    # ------------------------------------------------

    elif menu == "Create Student":

        st.subheader("Create Student")

        username = st.text_input("Student Username")
        password = st.text_input("Password", type="password")
        semester = st.number_input("Semester", 1, 8)
        gpa = st.number_input("Previous GPA", 0.0, 10.0)

        if st.button("Create Student"):

            cursor.execute(
                """
                INSERT INTO users (username, password, role, department)
                VALUES (?, ?, 'Student', 'CSE')
                """,
                (username, password)
            )

            user_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO students (user_id, semester, previous_gpa)
                VALUES (?, ?, ?)
                """,
                (user_id, semester, gpa)
            )

            conn.commit()

            st.success("Student created successfully")

    # ------------------------------------------------
    # CREATE SUBJECT
    # ------------------------------------------------

    elif menu == "Create Subject":

        st.subheader("Create Subject")

        subject_name = st.text_input("Subject Name")
        semester = st.number_input("Semester", 1, 8)

        if st.button("Create Subject"):

            cursor.execute(
                """
                INSERT INTO subjects (subject_name, semester)
                VALUES (?, ?)
                """,
                (subject_name, semester)
            )

            conn.commit()

            st.success("Subject created successfully")

    # ------------------------------------------------
    # ASSIGN TEACHER TO SUBJECT
    # ------------------------------------------------

    elif menu == "Assign Teacher to Subject":

        st.subheader("Assign Teacher")

        # get subjects
        cursor.execute("SELECT id, subject_name FROM subjects")
        subjects = cursor.fetchall()

        subject_dict = {name: sid for sid, name in subjects}

        subject_name = st.selectbox(
            "Select Subject",
            list(subject_dict.keys())
        )

        subject_id = subject_dict[subject_name]

        # get teachers
        cursor.execute("""
        SELECT teachers.id, users.username
        FROM teachers
        JOIN users ON teachers.user_id = users.id
        """)

        teachers = cursor.fetchall()

        teacher_dict = {name: tid for tid, name in teachers}

        teacher_name = st.selectbox(
            "Select Teacher",
            list(teacher_dict.keys())
        )

        teacher_id = teacher_dict[teacher_name]

        if st.button("Assign Teacher"):

            cursor.execute(
                """
                UPDATE subjects
                SET teacher_id=?
                WHERE id=?
                """,
                (teacher_id, subject_id)
            )

            conn.commit()

            st.success(f"{teacher_name} assigned to {subject_name}")