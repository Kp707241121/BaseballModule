# pages/5_🧭_Radar.py

import streamlit as st
import pandas as pd
import plotly.express as px
from getStats import compute_team_stats  # Dynamically load stats

# Constants
STAT_ORDER = ['R', 'HR', 'RBI', 'OBP', 'SB', 'K', 'W', 'SV', 'ERA', 'WHIP']
INVERT_STATS = {'ERA', 'WHIP', 'OBP'}  # Where lower is better

# Page Title
st.title("🧭 Multi-Team & Single-Team Radar Charts")

# Compute stats dynamically
@st.cache_data
def load_team_stats():
    data = compute_team_stats()
    df = pd.DataFrame.from_dict(data, orient="index")
    df.index.name = "Team"
    return df

df_stats = load_team_stats()

# Normalize stats (0–1 scale)
df_normalized = (df_stats - df_stats.min()) / (df_stats.max() - df_stats.min())

# Invert stats where lower is better
for stat in INVERT_STATS:
    if stat in df_normalized:
        df_normalized[stat] = 1 - df_normalized[stat]

# 🔷 Multi-Team Radar Chart
st.subheader("🔷 Multi-Team Radar Chart")

teams_selected = st.multiselect("Select Teams", df_normalized.index.tolist(), default=[df_normalized.index[0]])

if teams_selected:
    df_long = df_normalized.loc[teams_selected][STAT_ORDER].reset_index().melt(
        id_vars='Team', var_name='Stat', value_name='Value'
    )

    fig_multi = px.line_polar(
        df_long,
        r='Value',
        theta='Stat',
        color='Team',
        line_close=True,
        title="Team Comparison Radar (Normalized & Adjusted)"
    )
    fig_multi.update_traces(fill='toself')
    st.plotly_chart(fig_multi)
else:
    st.warning("Please select at least one team to display the radar chart.")

# 🔹 Single-Team Radar Chart
st.subheader("🔹 Single-Team Radar Chart")

team_selected = st.selectbox("Select Team", df_normalized.index)

fig_single = px.line_polar(
    r=df_normalized.loc[team_selected][STAT_ORDER],
    theta=STAT_ORDER,
    line_close=True,
    title=f"{team_selected} Stat Radar (Normalized)"
)
fig_single.update_traces(fill='toself')
st.plotly_chart(fig_single)
