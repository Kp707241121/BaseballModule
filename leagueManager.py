import os
from dotenv import load_dotenv
from espn_api.baseball import League
from custom_box_score import H2HCategoryBoxScore


class LeagueManager:
    def __init__(self, league_id: int, year: int):
        load_dotenv()
        self.espn_s2 = os.getenv("ESPN_S2")
        self.swid = os.getenv("SWID")
        self.league_id = league_id
        self.year = year
        self._connect()

    def _connect(self):
        self.league = League(
            league_id=self.league_id,
            year=self.year,
            espn_s2=self.espn_s2,
            swid=self.swid
        )
        self._patch_box_score_class()

    def _patch_box_score_class(self):
        self.league._box_score_class = H2HCategoryBoxScore

    def get_league(self):
        return self.league