from leagueManager import LeagueManager
from faStats import Player

# --- Constants ---
PITCHING_STATS = ['K', 'W', 'SV', 'ERA', 'WHIP']
HITTING_STATS = ['R', 'HR', 'RBI', 'OBP', 'SB']
DECIMAL_STATS = {"OBP", "ERA", "WHIP"}
POSITIONS = {"OF": 5, "DH": 11, "SP": 14, "RP": 15, "IF": 19}
SPLIT_TO_WEEK_OFFSET = {0: 0, 1: 7, 2: 15, 3: 30}

class FreeAgents:
    def __init__(self, league_manager: LeagueManager):
        self.league = league_manager.get_league()

    def get_free_agents(self, size=100, stat_split_type=1):
        agents = {}
        current_week = self.league.current_week
        target_week = max(1, current_week - SPLIT_TO_WEEK_OFFSET.get(stat_split_type, 0))

        for pos_label, pos_id in POSITIONS.items():
            try:
                fa_pool = self.league.free_agents(week=target_week, size=size, position_id=pos_id)
                agents[pos_label] = {}
                count = 0

                for player in fa_pool:
                    if not isinstance(player, Player):
                        continue
                    if player.injuryStatus != "ACTIVE":
                        continue

                    stat_keys = PITCHING_STATS if pos_label in {"SP", "RP"} else HITTING_STATS

                    stat_entry = player.stats.get((0, stat_split_type), {})
                    breakdown = stat_entry.get("breakdown", {})
                    print(f"{player.name} | {pos_label} | Breakdown: {breakdown}")

                    stat_line = {
                        stat: round(breakdown.get(stat, 0), 3) if stat in DECIMAL_STATS
                        else int(round(breakdown.get(stat, 0)))
                        for stat in stat_keys
                    }

                    if all(v == 0 for v in stat_line.values()):
                        print(f"⏩ Skipping {player.name} due to 0 stats: {stat_line}")
                        continue

                    agents[pos_label][player.name] = {
                        "position": pos_label,
                        "stats": stat_line
                    }

                    count += 1
                    if count >= 50:
                        break

            except Exception as e:
                print(f"⚠️ Error fetching free agents for {pos_label}: {e}")

        return agents
