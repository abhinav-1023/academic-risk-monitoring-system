import streamlit as st
import sqlite3
import os

# -----------------------------------
# DATABASE PATH
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(
    BASE_DIR,
    "..",
    "database",
    "college_system.db"
)

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

def get_connection():
    return sqlite3.connect(db_path)

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

    conn = get_connection()
    cursor = conn.cursor()

    # =================================================
    # CREATE TEACHER
    # =================================================

    if menu == "Create Teacher":

        st.subheader("Create Teacher")

        username = st.text_input("Teacher Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        department = st.text_input("Department")

        if st.button("Create Teacher"):

            try:

                cursor.execute(
                    """
                    INSERT INTO users
                    (username, password, role, department)
                    VALUES (?, ?, 'Teacher', ?)
                    """,
                    (
                        username,
                        password,
                        department
                    )
                )

                user_id = cursor.lastrowid

                cursor.execute(
                    """
                    INSERT INTO teachers
                    (user_id, department)
                    VALUES (?, ?)
                    """,
                    (
                        user_id,
                        department
                    )
                )

                conn.commit()

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

        semester = st.selectbox(
            "Current Semester",
            [1, 2, 3, 4, 5, 6, 7, 8]
        )

        if st.button("Create Student"):

            try:

                # Insert into users table
                cursor.execute(
                    """
                    INSERT INTO users
                    (username, password, role, department)
                    VALUES (?, ?, 'Student', 'CSE')
                    """,
                    (
                        username,
                        password
                    )
                )

                user_id = cursor.lastrowid

                # Insert into students table
                cursor.execute(
                    """
                    INSERT INTO students
                    (user_id, student_name, semester)
                    VALUES (?, ?, ?)
                    """,
                    (
                        user_id,
                        student_name,
                        semester
                    )
                )

                conn.commit()

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
            [1, 2, 3, 4, 5, 6, 7, 8]
        )

        if st.button("Create Subject"):

            try:

                cursor.execute(
                    """
                    INSERT INTO subjects
                    (subject_name, semester)
                    VALUES (?, ?)
                    """,
                    (
                        subject_name,
                        semester
                    )
                )

                conn.commit()

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

        cursor.execute(
            """
            SELECT id, subject_name
            FROM subjects
            """
        )

        subjects = cursor.fetchall()

        if not subjects:

            st.warning(
                "No subjects available"
            )

            return

        subject_dict = {
            name: sid
            for sid, name in subjects
        }

        subject_name = st.selectbox(
            "Select Subject",
            list(subject_dict.keys())
        )

        subject_id = subject_dict[subject_name]

        # -----------------------------------
        # FETCH TEACHERS
        # -----------------------------------

        cursor.execute(
            """
            SELECT teachers.id, users.username
            FROM teachers
            JOIN users
            ON teachers.user_id = users.id
            """
        )

        teachers = cursor.fetchall()

        if not teachers:

            st.warning(
                "No teachers available"
            )

            return

        teacher_dict = {
            name: tid
            for tid, name in teachers
        }

        teacher_name = st.selectbox(
            "Select Teacher",
            list(teacher_dict.keys())
        )

        teacher_id = teacher_dict[teacher_name]

        # -----------------------------------
        # ASSIGN BUTTON
        # -----------------------------------

        if st.button("Assign Teacher"):

            try:

                cursor.execute(
                    """
                    UPDATE subjects
                    SET teacher_id=?
                    WHERE id=?
                    """,
                    (
                        teacher_id,
                        subject_id
                    )
                )

                conn.commit()

                st.success(
                    f"{teacher_name} assigned to {subject_name}"
                )

            except Exception as e:

                st.error(f"Error: {e}")

    # -----------------------------------
    # CLOSE CONNECTION
    # -----------------------------------

    conn.close()