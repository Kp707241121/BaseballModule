# main.py
import streamlit as st

st.set_page_config(
    page_title="Fantasy Baseball Dashboard",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"  # 👈 Prevent sidebar from collapsing
)

st.title("⚾ Fantasy Baseball Dashboard")
st.markdown("""

- 🏆 Standings  
- 📅 Schedule            
- 📈 Team stats  
- 🧢 Rosters  

⬅️ Use the left sidebar to navigate between pages  
❗ Select 'USER' when prompted to log in ❗
""")

