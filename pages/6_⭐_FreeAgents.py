# pages/6_🧭_FreeAgents.py

import streamlit as st
import pandas as pd
import plotly.express as px
from login import login  # or adjust import path if needed
from leagueManager import LeagueManager
from free_agents import FreeAgents

# --- Restrict Page Access ---
if "role" not in st.session_state or st.session_state.role not in ["User", "Admin"]:
    st.warning("You must log in to access this page.")
    login()
    st.stop()
    
PITCHING_STATS = ['K', 'W', 'SV', 'ERA', 'WHIP']
HITTING_STATS = ['R', 'HR', 'RBI', 'OBP', 'SB']
INVERT_STATS = {'ERA', 'WHIP'}

# Load Free Agent Data
@st.cache_data
def load_free_agents():
    manager = LeagueManager(league_id=121531, year=2025)
    fa = FreeAgents(manager)
    return fa.get_free_agents()

if st.button("🔄 Refresh Free Agent Data"):
    st.cache_data.clear()
    st.rerun()

free_agents = load_free_agents()

# Helper to flatten dictionary into DataFrame
def flatten(fa_dict, stat_keys):
    data = []
    for position, players in fa_dict.items():
        for name, stats in players.items():
            if all(k in stats for k in stat_keys):
                entry = {"Player": name, "Position": position}
                entry.update({k: stats[k] for k in stat_keys})
                data.append(entry)
    return pd.DataFrame(data)

# Normalize stats
def normalize(df, stat_keys):
    df_norm = df.copy()
    for stat in stat_keys:
        min_val = df[stat].min()
        max_val = df[stat].max()
        if max_val != min_val:
            df_norm[stat] = (df[stat] - min_val) / (max_val - min_val)
        else:
            df_norm[stat] = 0.5
        if stat in INVERT_STATS:
            df_norm[stat] = 1 - df_norm[stat]
    return df_norm

# Split hitters and pitchers
pitch_df = flatten({k: v for k, v in free_agents.items() if k in {"SP", "RP"}}, PITCHING_STATS)
hit_df = flatten({k: v for k, v in free_agents.items() if k not in {"SP", "RP"}}, HITTING_STATS)

pitch_df_norm = normalize(pitch_df, PITCHING_STATS)
hit_df_norm = normalize(hit_df, HITTING_STATS)

# Streamlit UI
st.title("🧭 Free Agent Radar Charts")

st.subheader("Pitchers (SP & RP)")
pitchers = st.multiselect("Select Pitchers", pitch_df_norm["Player"].tolist())
if pitchers:
    long_df = pitch_df_norm[pitch_df_norm["Player"].isin(pitchers)].melt(
        id_vars="Player", value_vars=PITCHING_STATS, var_name="Stat", value_name="Value"
    )
    fig = px.line_polar(long_df, r="Value", theta="Stat", color="Player", line_close=True)
    fig.update_traces(fill='toself')
    st.plotly_chart(fig)

st.subheader("Hitters (Other Positions)")
hitters = st.multiselect("Select Hitters", hit_df_norm["Player"].tolist())
if hitters:
    long_df = hit_df_norm[hit_df_norm["Player"].isin(hitters)].melt(
        id_vars="Player", value_vars=HITTING_STATS, var_name="Stat", value_name="Value"
    )
    fig = px.line_polar(long_df, r="Value", theta="Stat", color="Player", line_close=True)
    fig.update_traces(fill='toself')
    st.plotly_chart(fig)
