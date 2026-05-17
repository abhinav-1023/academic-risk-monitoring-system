import streamlit as st

from utils.auth import authenticate

from modules.admin_panel import admin_dashboard
from modules.teacher_panel import teacher_dashboard
from modules.student_panel import student_dashboard


# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(

    page_title="AI Academic Risk Monitoring System",

    page_icon="🎓",

    layout="wide"
)

# ===================================
# SESSION STATE
# ===================================

if "role" not in st.session_state:

    st.session_state.role = None

if "username" not in st.session_state:

    st.session_state.username = None

# ===================================
# CUSTOM CSS
# ===================================

st.markdown("""

<style>

[data-testid="stAppViewContainer"] {

    background-color: #050816;
}

.main-title {

    text-align: center;

    font-size: 52px;

    font-weight: bold;

    color: white;

    margin-top: 20px;

    margin-bottom: 10px;
}

.sub-title {

    text-align: center;

    color: #94A3B8;

    font-size: 20px;

    margin-bottom: 40px;
}

.login-box {

    background-color: #0F172A;

    padding: 40px;

    border-radius: 20px;

    box-shadow: 0px 0px 25px rgba(0,0,0,0.4);
}

.stTextInput > div > div > input {

    background-color: #111827;

    color: white;

    border-radius: 10px;

    border: 1px solid #334155;

    padding: 12px;
}

.stButton > button {

    width: 100%;

    background: linear-gradient(
        90deg,
        #2563EB,
        #7C3AED
    );

    color: white;

    border: none;

    border-radius: 10px;

    padding: 12px;

    font-size: 18px;

    font-weight: bold;
}

.stButton > button:hover {

    background: linear-gradient(
        90deg,
        #1D4ED8,
        #6D28D9
    );

    color: white;
}

</style>

""", unsafe_allow_html=True)

# ===================================
# LOGIN PAGE
# ===================================

if st.session_state.role is None:

    st.markdown(

        """
        <div class="main-title">

        🎓 AI Academic Risk Monitoring System

        </div>
        """,

        unsafe_allow_html=True
    )

    st.markdown(

        """
        <div class="sub-title">

        Smart Student Performance Tracking and Early Warning Platform

        </div>
        """,

        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1.3, 1])

    with col2:

        st.markdown(
            '<div class="login-box">',
            unsafe_allow_html=True
        )

        st.subheader("Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(

            "Password",

            type="password"
        )

        st.markdown("")

        if st.button("Login"):

            role = authenticate(
                username,
                password
            )

            if role:

                st.session_state.role = role

                st.session_state.username = username

                st.success(
                    f"Welcome {username}"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

# ===================================
# MAIN DASHBOARD
# ===================================

else:

    st.sidebar.title("Navigation")

    st.sidebar.write(
        f"User: {st.session_state.username}"
    )

    st.sidebar.write(
        f"Role: {st.session_state.role}"
    )

    st.sidebar.markdown("---")

    # ===================================
    # ROUTING
    # ===================================

    if st.session_state.role == "Admin":

        admin_dashboard()

    elif st.session_state.role == "Teacher":

        teacher_dashboard()

    elif st.session_state.role == "Student":

        student_dashboard()

    else:

        st.error("Unknown Role")

    # ===================================
    # LOGOUT
    # ===================================

    st.sidebar.markdown("---")

    if st.sidebar.button("Logout"):

        st.session_state.role = None

        st.session_state.username = None

        st.rerun()