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
        self.__lookup_tables()

    def get_season_leagues(self, year):
        """
        Given a year it is returning a list of leagues (in json format) and
        :param year:
        :return list_leagues:
        """
        url = URL+"/v1/soccerseasons/?season="+year
        leagues = requests.get(url, headers=HEADERS)
        leagues.raise_for_status()
        list_leagues = []
        for league in leagues.json():
            valid = self.__is_cache_valid(league)
            if valid[0]:
                cache_league = valid[1]
                if not cache_league:
                    self._LOGGER.debug(league["caption"] + " not present on the cache")
                else:
                    league = cache_league
                    self._LOGGER.debug(league["caption"] + " valid on the cache")
            else:
                self._LOGGER.debug(league["caption"] + " not valid on the cache")
            list_leagues.append(league)
        return list_leagues

    def get_league(self, name):
        """
        Given the name of the league retrieve the id first and with that
        is going to return the json of the league and
        :param name:
        :return league:
        """
        self._LOGGER.debug("retrieve league id from name " + name)
        id = self.cache.get_league_id(name)
        url = URL + "/v1/soccerseasons/" + str(id)
        league = requests.get(url, headers=HEADERS)
        league.raise_for_status()
        valid = self.__is_cache_valid(league.json())
        if not valid[0]:
            self._LOGGER.debug(league.json()["caption"] + " not valid on the cache")
            self.cache.set_league(league.json()["caption"], league.json())
        return league.json()

    def get_teams_league(self, name):
        """
        Given the name of the league is returning the list of teams that are part of that and
        create two tables name_league:[id teams] and name_team:id
        :param name:
        :return list teams:
        """
        valid = self.__is_cache_valid(name)
        list_teams = self.cache.get_team_leagues(name)
        if valid[0] and list_teams:
            self._LOGGER.debug("league " + name + " valid on the cache")
            list_teams = self.cache.get_team_leagues(name)
        if not valid[0] and not list_teams:
            self._LOGGER.debug("league " + name + " not valid on the cache")
            self._LOGGER.debug("retrieve league id from name " + name)
            id = self.cache.get_league_id(name)
            url = URL + "/v1/soccerseasons/" + id + "/teams"
            self._LOGGER.debug(url)
            teams = requests.get(url, headers=HEADERS)
            teams.raise_for_status()
            list_teams, list_team_ids = [], []
            for team in teams.json()['teams']:
                self.cache.set_team(team['name'], team)
                self.cache.set_team_id(team['name'], team['id'])
                list_team_ids.append(team['id'])
                list_teams.append(team)
            self.cache.set_team_id_leagues(name, list_team_ids)
            self.cache.set_team_leagues(name, list_teams)
        return list_teams

    def get_team(self, name):
        """
        Given the name of the team retrieve the id first and with that
        is going to return the json of the team
        :param name:
        :return team:
        """
        id = self.__find_team_id(name)
        self._LOGGER.debug("retrieve list league-team ids")
        league_ids = self.cache.get_all_team_ids('league-team-ids')
        team = None
        if league_ids:
            league = None
            self._LOGGER.debug("look for match in list league-team ids")
            for k, v in league_ids.items():
                if id in v.decode('utf-8'):
                    league = k.decode('utf-8')
            if league:
                self._LOGGER.debug("match found in list league-team ids, validate the cache")
                valid = self.__is_cache_valid(league)
                if valid[0]:
                    team = self.cache.get_team(name)
        if not team:
            self._LOGGER.debug(id + " not found on league-team-ids table")
            self._LOGGER.debug("not possible to verify if the team is updated or not")
            self._LOGGER.debug("retrieve team using " + id + " from api")
            url = URL + "/v1/teams/" + str(id)
            team = requests.get(url, headers=HEADERS)
            team.raise_for_status()
            team = team.json()
            self.cache.set_team(team['name'], team)
            self.cache.set_team_id(team['name'], team['id'])
        return team

    def get_player_team(self, name, position=''):
        """
        Given the name of the team retrieve the id first and with that
        is going to return the json of the team players
        :param name: str team name
        :param position: str position optional
        :return:
        """
        id = self.__find_team_id(name)
        palyers = None
        if not palyers:
            self._LOGGER.debug("retrieve players of team using " + id + " from api")
            url = URL + "/v1/teams/" + str(id) + "/players"
            players = requests.get(url, headers=HEADERS)
            players.raise_for_status()
            players = players.json()
            if position:
                players_position = []
                for player in players['players']:
                    if player['position'] == position:
                        players_position.append(player)
                return players_position
            # self.cache.set_team(team['name'], team)
            # self.cache.set_team_id(team['name'], team['id'])
        return players

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
            self._LOGGER.debug("standing for " + name + " not valid on the cache, retrieve from api")
            standing = requests.get(url, headers=HEADERS)
            standing.raise_for_status()
            standing = standing.json()
            self.cache.set_standing(id, standing)
        self._LOGGER.debug("Load standings "+standing['leagueCaption'])
        return standing

    def __is_cache_valid(self, league):
        if isinstance(league, str) or str(type(league)) == "<type 'unicode'>":
            cache_league = self.cache.get_league(league)
            id = self.cache.get_league_id(league)
            url = URL + "/v1/soccerseasons/" + str(id)
            league = requests.get(url, headers=HEADERS).json()
        elif isinstance(league, dict):
            cache_league = self.cache.get_league(league["caption"])
        if cache_league:
            return [cache_league['lastUpdated'] >= league['lastUpdated'], cache_league]
        return [cache_league]

    def __lookup_tables(self):
        """
        Initialize lookuptables
        league_name:league_id
        :return:
        """
        for year in ['2015', '2016']:
            self._LOGGER.debug("set league-id lookup tables for " + year)
            url = URL + "/v1/soccerseasons/?season=" + year
            leagues = requests.get(url, headers=HEADERS)
            leagues.raise_for_status()
            for league in leagues.json():
                self.cache.set_league_id(league["caption"], league["id"])

    def __find_team_id(self, name):
        """
        Given a name of a team retrieve the id from the cache or looking in every season and league
        to find a correspondence
        :param name: str team name
        :return team_id: id
        """
        self._LOGGER.debug("retrieve team id from " + name)
        id = self.cache.get_team_id(name)
        if not id:
            self._LOGGER.debug("no team id correspondence for " + name)
            for year in ['2015', '2016', '2017']:
                for league in self.get_season_leagues(year):
                    for team in self.get_teams_league(league['caption']):
                        if team['name'] == name:
                            self._LOGGER.debug("found the league " + name)
                            id = team['id']
        return id
