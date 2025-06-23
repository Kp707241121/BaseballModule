
# pages/2_📈_Team_Stats.py

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import subprocess
from leagueManager import LeagueManager  # Module is directly in C:\BaseballModuleMAIN

# --- Constants ---
STAT_ORDER = ['R', 'HR', 'RBI', 'OBP', 'SB', 'K', 'W', 'SV', 'ERA', 'WHIP']
ASCENDING_STATS = {'ERA', 'WHIP'}
FLOAT_COLS = {'ERA', 'WHIP', 'OBP'}
FORMAT_DICT = {col: "{:.3f}" if col in FLOAT_COLS else "{:.0f}" for col in STAT_ORDER}

# --- Refresh Button ---
if st.button("🔄 Refresh Stats"):
    with st.spinner("Refreshing stats..."):
        result = subprocess.run(["python", "getStats.py"], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("✅ Stats refreshed successfully!")
        else:
            st.error("❌ Failed to refresh stats.")
            st.text(result.stderr)

# --- Load Stats ---
@st.cache_data
def load_team_stats():
    with open("team_stats.json") as f:
        return json.load(f)

team_stats = load_team_stats()
df_stats = pd.DataFrame.from_dict(team_stats, orient="index")
df_stats.index.name = "Team"
df_stats = df_stats[STAT_ORDER]

# --- Styled Table ---
st.title("📈 Accumulated Team Stats")
st.dataframe(df_stats.style.format(FORMAT_DICT), use_container_width=True)

# --- League Info ---
manager = LeagueManager(league_id=121531, year=2025)
league = manager.get_league()
logo_map = {team.team_name: team.logo_url for team in league.teams}

# --- Bar Chart ---
st.title("📊 Team Performance Charts")
selected_stat = st.selectbox("Choose a Stat to Compare", STAT_ORDER)

ascending = selected_stat in ASCENDING_STATS
df_sorted = df_stats.sort_values(by=selected_stat, ascending=ascending)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df_sorted.index, df_sorted[selected_stat], color='lightcoral')
ax.set_title(f"{selected_stat} by Team")
ax.set_xlabel("Team")
ax.set_ylabel(selected_stat)
plt.xticks(rotation=45)

for bar in bars:
    height = bar.get_height()
    label = FORMAT_DICT[selected_stat].format(height)
    offset = (df_sorted[selected_stat].max() - df_sorted[selected_stat].min()) * 0.01 or 0.1
    ax.text(bar.get_x() + bar.get_width() / 2, height + offset, label, ha='center', va='bottom')

st.pyplot(fig)

# --- Line Chart ---
selected_stat_line = st.selectbox("Choose a Stat to Plot Over Teams", STAT_ORDER, key="line_chart")
ascending = selected_stat_line in ASCENDING_STATS
df_sorted_line = df_stats.sort_values(by=selected_stat_line, ascending=ascending)

fig_line, ax_line = plt.subplots(figsize=(12, 6))
ax_line.plot(df_sorted_line.index, df_sorted_line[selected_stat_line], marker='o', linestyle='-')
ax_line.set_title(f"{selected_stat_line} by Team")
ax_line.set_xlabel("Team")
ax_line.set_ylabel(selected_stat_line)
plt.xticks(rotation=45)

st.pyplot(fig_line)

# --- Radar Line Chart (Normalized) ---
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(df_stats), columns=df_stats.columns, index=df_stats.index)
df_melt = df_normalized.reset_index().melt(id_vars='Team', var_name='Stat', value_name='Value')

fig_all = px.line(
    df_melt,
    x='Stat',
    y='Value',
    color='Team',
    line_group='Team',
    markers=True,
    title='Normalized Stat Comparison Across Teams'
)
st.plotly_chart(fig_all)


if st.button("🔄 Refresh Stats"):
    with st.spinner("Refreshing stats..."):
        result = subprocess.run(["python", "getStats.py"], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("✅ Stats refreshed successfully!")
        else:
            st.error("❌ Failed to refresh stats.")
            st.text(result.stderr)


STAT_ORDER = ['R', 'HR', 'RBI', 'OBP', 'SB', 'K', 'W', 'SV', 'ERA', 'WHIP']
ASCENDING_STATS = {'ERA', 'WHIP'}  

# Title
st.title("📈 Accumulated Team Stats")

# Load data
with open("team_stats.json") as f:
    team_stats = json.load(f)

# Convert to DataFrame
df = pd.DataFrame.from_dict(team_stats, orient="index")
df.index.name = "Team"
df = df[STAT_ORDER]  # Reorder columns

# Define formatting
float_cols = {'ERA', 'WHIP', 'OBP'}
format_dict = {col: "{:.3f}" if col in float_cols else "{:.0f}" for col in df.columns}

# Display styled DataFrame
st.dataframe(df.style.format(format_dict), use_container_width=True)


# --- Load Saved Stats ---
with open("team_stats.json") as f:
    team_stats = json.load(f)

df_stats = pd.DataFrame.from_dict(team_stats, orient='index')
df_stats.index.name = "Team"

# --- Load Logos Live ---
manager = LeagueManager(league_id=121531, year=2025)
league = manager.get_league()
logo_map = {team.team_name: team.logo_url for team in league.teams}

# --- Streamlit Page UI ---
st.title("📊 Team Performance Charts")

# --- Stat Selector & Bar Chart ---
selected_stat = st.selectbox("Choose a Stat to Compare", STAT_ORDER)

# Set sort order
ascending = True if selected_stat in ASCENDING_STATS else False

# Sort
df_sorted = df_stats.sort_values(by=selected_stat, ascending=ascending)

# Plot bar chart
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df_sorted.index, df_sorted[selected_stat], color='lightcoral')
ax.set_title(f"{selected_stat} by Team")
ax.set_xlabel("Team")
ax.set_ylabel(selected_stat)
plt.xticks(rotation=45)

# Add value labels
for bar in bars:
    height = bar.get_height()
    value = height
    fmt = format_dict[selected_stat]
    label = fmt.format(value)
    offset = (df_sorted[selected_stat].max() - df_sorted[selected_stat].min()) * 0.01 or 0.1
    ax.text(bar.get_x() + bar.get_width() / 2, height + offset, label, ha='center', va='bottom')

    
st.pyplot(fig)

# --- Line Chart ---
selected_stat = st.selectbox("Choose a Stat to Plot Over Teams", STAT_ORDER)

# Set sort order
ascending = True if selected_stat in ASCENDING_STATS else False

# Sort
df_sorted = df_stats.sort_values(by=selected_stat, ascending=ascending)

# Plot line chart
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_sorted.index, df_sorted[selected_stat], marker='o', linestyle='-')
ax.set_title(f"{selected_stat} by Team")
ax.set_xlabel("Team")
ax.set_ylabel(selected_stat)
plt.xticks(rotation=45)
st.pyplot(fig)

# Normalize stats 0-1 range
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(df_stats), 
                             columns=df_stats.columns,
                             index=df_stats.index)

# Melt for line plot
df_melt = df_normalized.reset_index().melt(id_vars='Team', var_name='Stat', value_name='Value')

fig_all = px.line(
    df_melt,
    x='Stat',
    y='Value',
    color='Team',
    line_group='Team',
    markers=True,
    title='Normalized Stat Comparison Across Teams'
)
st.plotly_chart(fig_all)
