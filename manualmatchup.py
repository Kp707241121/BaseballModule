import Matchup as BaseMatchup

class Scores(BaseMatchup):
    """Custom Matchup class to expose live scores."""
    def __init__(self, data, week=None):
        self.week = week
        self.home_team_live_score = None
        self.away_team_live_score = None
        self._fetch_matchup_info(data)

    def __repr__(self):
        if self.away_team_live_score is None:
            return f'Matchup({self.home_team}, {self.away_team})'
        return (f'Matchup({self.home_team} {round(self.home_team_live_score, 1)} - '
                f'{round(self.away_team_live_score, 1)} {self.away_team})')

    def _fetch_matchup_info(self, data):
        """Extract matchup data from ESPN API payload."""
        self.home_team = data['home']['teamId']
        self.home_final_score = data['home']['totalPoints']
        self.away_team = data['away']['teamId']
        self.away_final_score = data['away']['totalPoints']
        self.winner = data.get('winner')

        # Optional: extract live scores from cumulative stats
        try:
            if 'cumulativeScore' in data['home'] and data['home']['cumulativeScore']['scoreByStat']:
                self.home_team_live_score = (
                    data['home']['cumulativeScore'].get('wins', 0) +
                    data['home']['cumulativeScore'].get('ties', 0) / 2
                )
                self.away_team_live_score = (
                    data['away']['cumulativeScore'].get('wins', 0) +
                    data['away']['cumulativeScore'].get('ties', 0) / 2
                )
        except Exception as e:
            print(f"⚠️ Error parsing live score: {e}")
            self.home_team_live_score = None
            self.away_team_live_score = None
