# pages/2_📈_Team_Stats.py

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import subprocess
import sys
import os
from leagueManager import LeagueManager

# --- Constants ---
STAT_ORDER = ['R', 'HR', 'RBI', 'OBP', 'SB', 'K', 'W', 'SV', 'ERA', 'WHIP']
ASCENDING_STATS = {'ERA', 'WHIP'}
FLOAT_COLS = {'OBP', 'ERA', 'WHIP'}
FORMAT_DICT = {stat: "{:.3f}" if stat in FLOAT_COLS else "{:.0f}" for stat in STAT_ORDER}

# --- Page Title ---
st.title("📈 Accumulated Team Stats")

# --- Refresh Button ---
if st.button("🔄 Refresh Stats"):
    with st.spinner("Refreshing stats..."):
        result = subprocess.run(["python", "getStats.py"], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("✅ Stats refreshed successfully!")
        else:
            st.error("❌ Failed to refresh stats.")
            st.text(result.stderr)

# --- Load JSON Data ---
@st.cache_data
def load_team_stats(path="team_stats.json"):
    with open(path) as f:
        return json.load(f)

team_stats = load_team_stats()
df = pd.DataFrame.from_dict(team_stats, orient="index")
df.index.name = "Team"
df = df[STAT_ORDER]
df_stats = df.copy()

# --- Data Table ---
st.subheader("📋 Team Stat Table")
st.dataframe(df.style.format(FORMAT_DICT), use_container_width=True)

# --- League Info for Logos (Optional) ---
manager = LeagueManager(league_id=121531, year=2025)
league = manager.get_league()
logo_map = {team.team_name: team.logo_url for team in league.teams}

# --- Bar Chart ---
st.subheader("📊 Bar Chart Comparison")
selected_bar_stat = st.selectbox("Choose a stat for bar chart", STAT_ORDER, key="bar_chart")
bar_ascending = selected_bar_stat in ASCENDING_STATS
df_sorted_bar = df_stats.sort_values(by=selected_bar_stat, ascending=bar_ascending)

fig_bar, ax_bar = plt.subplots(figsize=(12, 6))
bars = ax_bar.bar(df_sorted_bar.index, df_sorted_bar[selected_bar_stat], color='steelblue')
ax_bar.set_title(f"{selected_bar_stat} by Team")
ax_bar.set_xlabel("Team")
ax_bar.set_ylabel(selected_bar_stat)
plt.xticks(rotation=45)

# Add labels above bars
for bar in bars:
    height = bar.get_height()
    label = FORMAT_DICT[selected_bar_stat].format(height)
    offset = (df_sorted_bar[selected_bar_stat].max() - df_sorted_bar[selected_bar_stat].min()) * 0.01 or 0.1
    ax_bar.text(bar.get_x() + bar.get_width() / 2, height + offset, label, ha='center', va='bottom')

st.pyplot(fig_bar)

# --- Line Chart ---
st.subheader("📈 Line Chart Comparison")
selected_line_stat = st.selectbox("Choose a stat for line chart", STAT_ORDER, key="line_chart")
line_ascending = selected_line_stat in ASCENDING_STATS
df_sorted_line = df_stats.sort_values(by=selected_line_stat, ascending=line_ascending)

fig_line, ax_line = plt.subplots(figsize=(12, 6))
ax_line.plot(df_sorted_line.index, df_sorted_line[selected_line_stat], marker='o')
ax_line.set_title(f"{selected_line_stat} by Team")
ax_line.set_xlabel("Team")
ax_line.set_ylabel(selected_line_stat)
plt.xticks(rotation=45)

st.pyplot(fig_line)

# --- Radar-style Normalized Line Plot ---
st.subheader("📊 Normalized Stat Comparison (Radar Style)")
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(
    scaler.fit_transform(df_stats),
    columns=df_stats.columns,
    index=df_stats.index
)

df_melted = df_normalized.reset_index().melt(id_vars="Team", var_name="Stat", value_name="Value")

fig_radar = px.line(
    df_melted,
    x="Stat",
    y="Value",
    color="Team",
    line_group="Team",
    markers=True,
    title="Normalized Stat Comparison Across Teams"
)
fig_radar.update_traces(fill='toself')
st.plotly_chart(fig_radar)
