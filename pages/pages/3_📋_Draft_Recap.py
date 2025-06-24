import streamlit as st
import pandas as pd
from draftSummary import get_draft_summary

st.title("📋 Draft Recap")

# Get team-round-player data
summary = get_draft_summary()

# Get full set of team names and round numbers
teams = sorted(summary.keys())
rounds = sorted({rnd for team in summary.values() for rnd in team})

# Build a DataFrame with rounds as index and team names as columns
data = {team: [summary[team].get(rnd, [""])[0] if summary[team].get(rnd) else "" for rnd in rounds] for team in teams}
df = pd.DataFrame(data, index=[f"Round {rnd}" for rnd in rounds])

row_height = 35  # px per row (estimate)
st.dataframe(df, use_container_width=True, height=row_height * len(df) + 60)
