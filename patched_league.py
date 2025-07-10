from espn_api.baseball import League
import json
from faStats import Player, POSITION_MAP  # your custom Player class

class PatchedLeague(League):
    def free_agents(self, week=None, size=50, position=None, position_id=None):
        if self.year < 2019:
            raise Exception('Cant use free agents before 2019')
        if not week:
            week = self.current_week

        slot_filter = []
        if position and position in POSITION_MAP:
            slot_filter = [POSITION_MAP[position]]
        if position_id:
            slot_filter.append(position_id)

        params = {
            'view': ['kona_player_info', 'kona_player_recent_stats'],
            'scoringPeriodId': week,
        }
        filters = {
            "players": {
                "filterStatus": {"value": ["FREEAGENT", "WAIVERS"]},
                "filterSlotIds": {"value": slot_filter},
                "limit": size,
                "sortPercOwned": {"sortPriority": 1, "sortAsc": False},
                "sortDraftRanks": {"sortPriority": 100, "sortAsc": True, "value": "STANDARD"}
            }
        }
        headers = {'x-fantasy-filter': json.dumps(filters)}
        data = self.espn_request.league_get(params=params, headers=headers)
        return [Player(player, self.year) for player in data['players']]
