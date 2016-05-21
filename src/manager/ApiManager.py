import requests
from manager.CacheManager import CacheManager
import logging
import logging.config
logging.config.fileConfig("logging.conf")

URL = "http://api.football-data.org"
KEY = "fd7fafc8f9ad4d2cb86a0615335e6d79"
HEADERS = {'X-Auth-Token': KEY, 'X-Response-Control': "minified"}


class ApiManager():
    """
    Class that interact with soccer API http://api.football-data.org/
    """
    _LOGGER = logging.getLogger('API_MANAGER')

    def __init__(self):
        self.cache = CacheManager()

    def get_season_leagues(self, year):
        url = URL+"/v1/soccerseasons/?season="+year
        leagues = requests.get(url, headers=HEADERS)
        leagues.raise_for_status()
        list_leagues = []

        for league in leagues.json():
            valid = self.__is_cache_valid(league)
            if valid[0]:
                cache_league = valid[1]
                self._LOGGER.debug(valid[1]["caption"] + " valid on the cache")
                if not cache_league: #not sure if necessary
                    self._LOGGER.debug(league["caption"] + " not present on the cache")
                    self.cache.set_league(league["caption"], league)
                else:
                    league = cache_league
            else:
                self._LOGGER.debug(league["caption"] + " not valid on the cache")
                self.cache.set_league(league["caption"], league)
            list_leagues.append(league)
        return list_leagues

    def get_team(self, id):
        url = URL+"/v1/teams/"+str(id)
        team = requests.get(url, headers=HEADERS)
        team.raise_for_status()
        self._LOGGER.debug("Load team "+team.json()['name']+" data")
        return team.json()

    def get_league_table(self, id):
        url = URL+"/v1/soccerseasons/"+str(id)+"/leagueTable"
        table = requests.get(url, headers=HEADERS)
        table.raise_for_status()
        self._LOGGER.debug("Load table "+table.json()['leagueCaption']+" data")
        return table.json()

    def __is_cache_valid(self, league):
        cache_league = self.cache.get_league(league['caption'])
        if cache_league:
            return [cache_league['lastUpdated'] >= league['lastUpdated'], cache_league]
        return [cache_league]


