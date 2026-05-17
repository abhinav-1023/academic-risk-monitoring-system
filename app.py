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
# CUSTOM CSS
# ===================================

st.markdown("""
<style>

[data-testid="stSidebar"]{
    background-color:#1e1e2f;
}

.main-title{
    font-size:48px;
    font-weight:700;
    color:white;
    margin-bottom:10px;
}

.subtitle{
    color:#aaaaaa;
    font-size:18px;
    margin-bottom:40px;
}

.login-card{
    background:#111827;
    padding:40px;
    border-radius:20px;
    box-shadow:0px 0px 25px rgba(0,0,0,0.4);
}

.stButton>button{
    width:100%;
    border-radius:12px;
    height:50px;
    font-size:18px;
    font-weight:600;
    background:linear-gradient(
        90deg,
        #4f46e5,
        #7c3aed
    );
    color:white;
    border:none;
}

.stButton>button:hover{
    opacity:0.9;
}

.metric-card{
    background:#111827;
    padding:20px;
    border-radius:16px;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ===================================
# SESSION VARIABLES
# ===================================

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

# ===================================
# LOGIN PAGE
# ===================================

if st.session_state.role is None:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("""
        <div class="main-title">
        🎓 AI Academic Risk Monitoring System
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="subtitle">
        AI-Powered Early Warning and Student Performance Monitoring
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.subheader("Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

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
                    "Invalid username or password"
                )

        st.markdown("</div>", unsafe_allow_html=True)

# ===================================
# DASHBOARD
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
    # ROLE ROUTING
    # ===================================

    if st.session_state.role == "Academic Coordinator":

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