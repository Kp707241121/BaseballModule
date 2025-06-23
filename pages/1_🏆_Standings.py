import streamlit as st
import pandas as pd
from leagueManager import LeagueManager
from teams import Team
from manualmatchup import Scores# ✅ Use your custom Matchup subclass
# Inject your patched Scores logic into ESPN League
from espn_api.baseball import League
League._matchup_class = Scores  # ✅ Force all matchups to use your patched class

# --- Header ---
st.header("🏆 League Standings")

# --- Init league ---
manager = LeagueManager(league_id=121531, year=2025)
league = manager.get_league()

# --- Standings ---
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
schedule_data = []

# Pick team
team_names = [team.team_name for team in league.teams]
selected_team_name = st.selectbox("Select a team to view schedule:", team_names)
selected_team = next(team for team in league.teams if team.team_name == selected_team_name)

# Display team schedule
st.subheader(f"Schedule for {selected_team_name}")
for week_number, matchup in enumerate(selected_team.schedule, start=1):
    if matchup.home_team == selected_team:
        opponent = matchup.away_team
        location = "Home"
        score = matchup.home_team_live_score
        opp_score = matchup.away_team_live_score
    else:
        opponent = matchup.home_team
        location = "Away"
        score = matchup.away_team_live_score
        opp_score = matchup.home_team_live_score

    opponent_name = opponent.team_name if opponent else "BYE"

    schedule_data.append({
        "Week": week_number,  # ✅ Now explicitly tracking week
        "Opponent": opponent_name,
        "Score": score,
        "OpponentScore": opp_score
    })

# Display
df = pd.DataFrame(schedule_data).sort_values(by="Week")
df["Result"] = df.apply(
    lambda row: "W" if row["Score"] > row["OpponentScore"]
    else "L" if row["Score"] < row["OpponentScore"]
    else "T" if row["Score"] == row["OpponentScore"]
    else "Pending",
    axis=1
)
st.dataframe(df, use_container_width=True, hide_index=True)


# --- Final Standings Display ---

st.title("🏆 Final Standings (2024)")
st.dataframe(df, use_container_width=True, hide_index=true)
# For 2024 final standings
Priormanager = LeagueManager(league_id=121531, year=2024)
Priorleague = Priormanager.get_league()

final_standings = sorted(
    [team for team in Priorleague.teams if team.final_standing < 4],
    key=lambda t: t.final_standing
)

df = pd.DataFrame([{
    "Rank": i + 1,
    "Team": team.team_name,
    "Final Standing": team.final_standing
} for i, team in enumerate(final_standings)])

