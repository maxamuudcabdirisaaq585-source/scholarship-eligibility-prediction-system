import streamlit as st
import pickle
import numpy as np
import base64

# ----------------------------
# Login Background
# ----------------------------
def login_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        .login-box {{
            background-color: rgba(255,255,255,0.95);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# System Background
# ----------------------------
def system_background():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        h1 {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# Load Model
# ----------------------------
model = pickle.load(open("scholarship_model.pkl", "rb"))

# ----------------------------
# Session State
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ----------------------------
# LOGIN PAGE
# ----------------------------
if not st.session_state.logged_in:

    login_background("background.png")

    st.markdown(
        """
        <div class="login-box">
            <h1 style="color:black;">
                🎓 Scholarship Eligibility Prediction System
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# ----------------------------
# MAIN SYSTEM
# ----------------------------
else:

    system_background()

    st.title("🎓 Scholarship Prediction")

    gpa = st.number_input("GPA", min_value=0.0, max_value=4.0, value=0.0)
    income = st.number_input("Family Income", min_value=0.0)
    attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0)
    study_hours = st.number_input("Study Hours", min_value=0.0)
    activities = st.number_input("Activities", min_value=0.0)

    if st.button("Predict"):
        data = np.array([[gpa, income, attendance, study_hours, activities]])
        result = model.predict(data)

        if result[0] == 1:
            st.success("✅ Eligible for Scholarship")
        else:
            st.error("❌ Not Eligible")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()