import streamlit as st
import pandas as pd
from leagueManager import LeagueManager
from manualmatchup import Scores  # ✅ Your custom Matchup class

# Inject custom Scores logic into ESPN API
from espn_api.baseball import League
League._matchup_class = Scores

# Initialize League
manager = LeagueManager(league_id=121531, year=2025)
league = manager.get_league()

# --- Standings ---
st.header("🏆 League Standings")

standings = league.standings()
df_standings = pd.DataFrame([{
    "Overall": idx + 1,
    "Logo": team.logo_url,
    "Team": team.team_name,
    "Wins": team.wins,
    "Losses": team.losses,
    "Ties": team.ties
} for idx, team in enumerate(standings)])

st.data_editor(
    df_standings,
    column_config={
        "Logo": st.column_config.ImageColumn("Team Logo", width="small")
    },
    hide_index=True,
    use_container_width=True
)

# --- Schedule Viewer ---
st.title("📅 Team Schedule Viewer")

team_names = [team.team_name for team in league.teams]
selected_team_name = st.selectbox("Select a team to view schedule:", team_names)
selected_team = next(team for team in league.teams if team.team_name == selected_team_name)

schedule_data = []
st.subheader(f"Schedule for {selected_team_name}")

for m in selected_team.schedule:
    if m.home_team == selected_team:
        opponent = m.away_team
        location = "Home"
        score = m.home_team_live_score
        opp_score = m.away_team_live_score
    else:
        opponent = m.home_team
        location = "Away"
        score = m.away_team_live_score
        opp_score = m.home_team_live_score

    week = getattr(m, "matchup_period", getattr(m, "week", None))  # fallback if needed
    result = (
        "W" if score > opp_score else
        "L" if score < opp_score else
        "T" if score == opp_score else
        "Pending"
    )

    schedule_data.append({
        "Week": week,
        "Opponent": opponent.team_name if opponent else "BYE",
        "Location": location,
        "Score": score,
        "OpponentScore": opp_score,
        "Result": result
    })

df_schedule = pd.DataFrame(schedule_data).sort_values(by="Week")
st.dataframe(df_schedule, use_container_width=True)
