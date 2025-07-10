from leagueManager import LeagueManager
from free_agents import FreeAgents

manager = LeagueManager(league_id=121531, year=2025)
fa = FreeAgents(manager)

free_agents = fa.get_free_agents()

# Print top 3 agents in each position group
for pos, agents in free_agents.items():
    print(f"\n{pos}:")
    for name in list(agents.values())[:3]:
        print("  ", name)

