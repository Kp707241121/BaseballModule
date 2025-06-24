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

# --- Load precomputed free agents ---
with open("free_agents.json", "r", encoding="utf-8") as f:
    free_agents = json.load(f)

st.title("🆓 Free Agents")

for position, players in free_agents.items():
    st.subheader(position)
    for player_id, player_name in players.items():
        st.markdown(f"- {player_name} (ID: {player_id})")
