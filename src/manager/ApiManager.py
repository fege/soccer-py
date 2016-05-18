import requests
from datetime import datetime
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
            last_update = datetime.strptime(league['lastUpdated'], '%Y-%m-%dT%H:%M:%SZ')
            if last_update < datetime.now():
                self._LOGGER.debug(league["caption"]+" not updated on api")
                leag = self.cache.get_league(league["caption"])
                if not leag:
                    self._LOGGER.debug(league["caption"] + " not present on the cache")
                    self.cache.set_league(league["caption"], league)
                    list_leagues.append(league)
                else:
                    list_leagues.append(leag)
            else:
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
