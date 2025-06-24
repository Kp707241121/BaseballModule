# login.py or auth.py
import streamlit as st

def login():
    st.title("🔐 Login")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None

    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "admin" and password == st.secrets["ADMIN_PASSWORD"]:
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.success("✅ Logged in as Admin")
            else:
                st.error("❌ Invalid credentials")



