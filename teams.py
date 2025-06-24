class Team:
    def __init__(self, league, team_index: int):
        self.league = league
        self.team_index = team_index

    def get_roster(self):
        team = self.league.teams[self.team_index]
        return [
            {
                "name": player.name,
                "playerId": getattr(player, "playerId", None),
                "position": getattr(player, "lineupSlot", None),  # Use lineupSlot as position
                "eligibleSlots": getattr(player, "eligibleSlots", None),
                "injuryStatus": getattr(player, "injuryStatus", None),
            }
            for player in team.roster
        ]

    def get_team_name(self):
        return self.league.teams[self.team_index].team_name