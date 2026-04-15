import streamlit as st

from utils.auth import authenticate
from modules.admin_panel import admin_dashboard
from modules.teacher_panel import teacher_dashboard
from modules.student_panel import student_dashboard

from utils.database import initialize_database
initialize_database()



# PAGE CONFIG


st.set_page_config(
    page_title="AI Academic Risk Monitoring System",
    layout="wide"
)

st.title("🎓 AI‑Based Academic Risk Monitoring and Early Warning System")



# SESSION VARIABLES


if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None



# LOGIN PAGE


if st.session_state.role is None:

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        role = authenticate(username, password)

        if role:

            st.session_state.role = role
            st.session_state.username = username

            st.success(f"Logged in as {role}")

            st.rerun()

        else:

            st.error("Invalid username or password")



# DASHBOARD ROUTING


else:

    st.sidebar.title("Navigation")

    st.sidebar.write("User:", st.session_state.username)
    st.sidebar.write("Role:", st.session_state.role)

    st.sidebar.markdown("---")

    if st.session_state.role == "Academic Coordinator":

        admin_dashboard()

    elif st.session_state.role == "Teacher":

        teacher_dashboard()

    elif st.session_state.role == "Student":

        student_dashboard()

    else:

        st.error("Unknown role")



# LOGOUT

    st.sidebar.markdown("---")

    if st.sidebar.button("Logout"):

        st.session_state.role = None
        st.session_state.username = None

        st.rerun()