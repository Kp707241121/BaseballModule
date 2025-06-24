import streamlit as st
import pandas as pd
from draftSummary import get_draft_summary

st.title("📋 Draft Recap")

# Get team-round-player data
summary = get_draft_summary()

# Define static team order (manual or preserved)
# Define your desired team order
teams = ["Jameis' Crab Shack", "Uncle Juniors", "Wandering Franco", "Dodger Dogs","The Fighting Elvises", "Ball Tickler", "Trojan Kongs", "So Much (For) Fooly Cooly", "Steven's Super Team", "Wahoo Lives"]  # Replace with actual team names in desired order

# Get all unique round numbers
rounds = sorted({rnd for team in summary.values() for rnd in team})

# Build DataFrame
data = {
    team: [
        summary[team].get(rnd, [""])[0] if summary[team].get(rnd) else ""
        for rnd in rounds
    ]
    for team in teams
}
df = pd.DataFrame(data, index=[f"Round {rnd}" for rnd in rounds])

# Display with appropriate height
row_height = 35
st.dataframe(df, use_container_width=True, height=row_height * len(df) + 60)

