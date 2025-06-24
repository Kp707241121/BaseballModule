import streamlit as st

def login():
    # Dropdown for selecting role
    role = st.selectbox("Select role", ["User", "Admin"], key="role_select")

    if role == "Admin":
        password = st.text_input("Enter Admin Password", type="password")
        if password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.role = "Admin"
            st.success("✅ Access granted as Admin")
        elif password:
            st.error("❌ Incorrect password")
    else:
        st.session_state.role = "User"
        st.success("✅ Access granted as User")
