# pages/6_⭐_FreeAgents.py

import streamlit as st
import pandas as pd
from leagueManager import LeagueManager, FreeAgents

# --- Init league ---
manager = LeagueManager(league_id=121531, year=2025)
fa_manager = FreeAgents(manager)  # ✅ pass the instance, not the class

# --- Get free agents ---
free_agents = fa_manager.get_free_agents()

# --- Display ---
st.title("⭐ Free Agents by Position")

positions = list(free_agents.keys())
selected_position = st.selectbox("Choose a position", positions)

if selected_position:
    fa_dict = free_agents[selected_position]
    df = pd.DataFrame(fa_dict.items(), columns=["Player ID", "Player Name"])
    st.dataframe(df)