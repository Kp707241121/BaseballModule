# pages/6_⭐_FreeAgents.py

import streamlit as st
import json
import pandas as pd
import plotly.express as px
from login import login  # or adjust import path if needed

st.title("🔐 Admin Page: Free Agents")
# If role not set or not Admin, enforce login
if st.session_state.get("role") != "Admin":
    st.warning("🔒 Admin access required")
    login()
    st.stop()
