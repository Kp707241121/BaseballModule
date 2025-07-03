import streamlit as st
import pandas as pd
import plotly.express as px
from getStats import compute_team_stats
from sklearn.preprocessing import MinMaxScaler

# --- Constants ---
STAT_ORDER = ['R', 'HR', 'RBI', 'OBP', 'SB', 'K', 'W', 'SV', 'ERA', 'WHIP']
INVERT_STATS = {'ERA', 'WHIP'}

# --- Title ---
st.title("🧭 Team Stat Radar Charts")

# --- Load and Normalize Stats ---
team_stats = compute_team_stats()
df_stats = pd.DataFrame.from_dict(team_stats, orient='index')
df_stats.index.name = "Team"
df_stats = df_stats[STAT_ORDER]

# Normalize
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(
    scaler.fit_transform(df_stats),
    columns=STAT_ORDER,
    index=df_stats.index
)

# Invert ERA & WHIP
for stat in INVERT_STATS:
    if stat in df_normalized.columns:
        df_normalized[stat] = 1 - df_normalized[stat]

# --- Multi-Team Radar ---
st.subheader("📡 Multi-Team Radar")

teams_selected = st.multiselect("Select Teams", df_normalized.index, default=[df_normalized.index[0]])

if teams_selected:
    df_long = df_normalized.loc[teams_selected].reset_index().melt(
        id_vars='Team', var_name='Stat', value_name='Value'
    )
    fig_multi = px.line_polar(
        df_long,
        r='Value',
        theta='Stat',
        color='Team',
        line_close=True,
        title="Team Comparison Radar (Normalized)"
    )
    fig_multi.update_traces(fill='toself')
    st.plotly_chart(fig_multi)
else:
    st.warning("Please select at least one team to display the radar chart.")

# --- Single-Team Radar ---
st.subheader("🎯 Single-Team Radar")

team_selected = st.selectbox("Select Team", df_normalized.index)

fig_single = px.line_polar(
    r=df_normalized.loc[team_selected][STAT_ORDER],
    theta=STAT_ORDER,
    line_close=True,
    title=f"{team_selected} Stat Radar (Normalized)"
)
fig_single.update_traces(fill='toself')
st.plotly_chart(fig_single)
