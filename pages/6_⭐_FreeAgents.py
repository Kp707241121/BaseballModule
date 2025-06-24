# pages/6_⭐_FreeAgents.py

import streamlit as st
import json
import pandas as pd
import plotly.express as px
from login import login  # or adjust import path if needed

# --- Restrict Page Access ---
if "role" not in st.session_state or st.session_state.role not in ["Admin"]:
    st.warning("You must log in to access this page.")
    login()
    st.stop()