# pages/6_⭐_FreeAgents.py

import streamlit as st
import json
import pandas as pd
import plotly.express as px

# --- Load precomputed free agents ---
with open("free_agents.json", "r", encoding="utf-8") as f:
    free_agents = json.load(f)

st.title("🆓 Free Agents")

for position, players in free_agents.items():
    st.subheader(position)
    for player_id, player_name in players.items():
        st.markdown(f"- {player_name} (ID: {player_id})")
