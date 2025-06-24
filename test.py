from collections import defaultdict
from leagueManager import LeagueManager
from espn_api.baseball.league import League as lg
import json

# Initialize league connection
manager = LeagueManager(league_id=121531, year=2025)
d = lg(league_id=121531, year=2025, espn_s2=manager.espn_s2, swid=manager.swid)

# Build player ID → name map from all rosters and free agents
player_map = {}
for team in d.teams:
    for player in team.roster:
        player_map[player.playerId] = player.name
for player in d.free_agents(size=500):
    player_map[player.playerId] = player.name

# Build team ID → name map
team_map = {team.team_id: team.team_name for team in d.teams}

# Load and parse draft data
raw_draft = d.espn_request.get_league_draft()
if isinstance(raw_draft, str):
    raw_draft = json.loads(raw_draft)
picks = raw_draft.get("draftDetail", {}).get("picks", [])

# Group picks by teamId → roundId
draft_by_team = defaultdict(lambda: defaultdict(list))
for pick in picks:
    team_id = pick.get("teamId")
    round_id = pick.get("roundId")
    draft_by_team[team_id][round_id].append(pick)

# Print grouped summary with team names
for team_id in sorted(draft_by_team):
    team_name = team_map.get(team_id, f"Team {team_id}")
    print(f"\n🧢 {team_name} (ID: {team_id})")
    for round_id in sorted(draft_by_team[team_id]):
        for pick in draft_by_team[team_id][round_id]:
            pid = pick.get("playerId")
            name = pick.get("playerName") or player_map.get(pid, f"Player {pid}")
            print(f"  🌀 Round {round_id}: {name}")
