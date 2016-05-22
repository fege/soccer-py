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
                if not cache_league:
                    self._LOGGER.debug(league["caption"] + " not present on the cache")
                    self.cache.set_league(league["caption"], league)
                    self.cache.set_league_id(league["caption"], league["id"])
                else:
                    league = cache_league
            else:
                self._LOGGER.debug(league["caption"] + " not valid on the cache")
                self.cache.set_league(league["caption"], league)
                self.cache.set_league_id(league["caption"], league["id"])
            list_leagues.append(league)
        return list_leagues

    def get_league_table(self, name):
        self._LOGGER.debug("retrieve league id from name " + name)
        id = self.cache.get_league_id(name)
        league = self.get_league(name)
        valid = self.__is_cache_valid(league)
        self._LOGGER.debug("retrieve standing from id " + id)
        url = URL + "/v1/soccerseasons/" + id + "/leagueTable"
        if valid[0]:
            self._LOGGER.debug(valid[1]["caption"] + " valid on the cache")
            standing = self.cache.get_standing(id)
            if not standing:
                self._LOGGER.debug("no standing on the cache")
                standing = requests.get(url, headers=HEADERS)
                standing.raise_for_status()
                standing = standing.json()
                self.cache.set_standing(id, standing)
        else:
            self._LOGGER.debug("standing for " + name + " not valid on the cache, retrive from api")
            standing = requests.get(url, headers=HEADERS)
            standing.raise_for_status()
            standing = standing.json()
            self.cache.set_standing(id, standing)
        self._LOGGER.debug("Load standings "+standing['leagueCaption'])
        return standing

    def get_league(self, name):
        self._LOGGER.debug("retrieve league id from name " + name)
        id = self.cache.get_league_id(name)
        url = URL + "/v1/soccerseasons/" + str(id)
        league = requests.get(url, headers=HEADERS)
        league.raise_for_status()
        valid = self.__is_cache_valid(league.json())
        if valid[0]:
            league = valid[1]
            self._LOGGER.debug(valid[1]["caption"] + " valid on the cache")
        else:
            self._LOGGER.debug(league["caption"] + " not valid on the cache")
            self.cache.set_league(league["caption"], league.json())
            self.cache.set_league_id(league["caption"], league["id"])
        return league

    def get_team(self, id):
        url = URL+"/v1/teams/"+str(id)
        team = requests.get(url, headers=HEADERS)
        team.raise_for_status()
        self._LOGGER.debug("Load team "+team.json()['name']+" data")
        return team.json()

    def __is_cache_valid(self, league):
        cache_league = self.cache.get_league(league["caption"])
        if cache_league:
            return [cache_league['lastUpdated'] >= league['lastUpdated'], cache_league]
        return [cache_league]


