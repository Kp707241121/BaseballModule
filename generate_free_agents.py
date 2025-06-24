# generate_free_agents.py
from leagueManager import LeagueManager, FreeAgents

manager = LeagueManager(league_id=121531, year=2025)
fa = FreeAgents(manager)
fa.save_to_json("free_agents.json")
