from espn_api.baseball import Matchup as Basematchup

class Scores(Basematchup):
    '''Creates Matchup instance'''
    def __init__(self, data, week=None):
        self.week = week
        self.home_team_live_score = None
        self.away_team_live_score = None
        self._fetch_matchup_info(data)

    def __repr__(self):
        if not self.away_team_live_score:
            return 'Matchup(%s, %s)' % (self.home_team, self.away_team)
        else:
            return 'Matchup(%s %s - %s %s)' % (
                self.home_team,
                str(round(self.home_team_live_score, 1)),
                str(round(self.away_team_live_score, 1)),
                self.away_team
            )

    def _fetch_matchup_info(self, data):
        self.home_team = data['home']['teamId']
        self.home_final_score = data['home']['totalPoints']
        self.away_team = data['away']['teamId']
        self.away_final_score = data['away']['totalPoints']
        self.winner = data['winner']

        # ✅ Assign the week to matchup_period
        self.matchup_period = self.week

        if 'cumulativeScore' in data['home'] and data['home']['cumulativeScore']['scoreByStat']:
            self.home_team_live_score = (
                data['home']['cumulativeScore']['wins'] +
                data['home']['cumulativeScore']['ties'] / 2
            )
            self.away_team_live_score = (
                data['away']['cumulativeScore']['wins'] +
                data['away']['cumulativeScore']['ties'] / 2
            )