import json
import logging
import logging.config
logging.config.fileConfig("logging.conf")


class CacheManager():
    """
    Class that interact with Driver
    """
    _LOGGER = logging.getLogger('CACHE_MANAGER')

    def __init__(self):
        resource = "storage.RedisDriver"
        resource_mod = __import__(resource, globals(), locals(), ['RedisDriver'])
        cache = getattr(resource_mod, 'RedisDriver')
        self.cache = cache()

    def set_league(self, field, value):
        self._LOGGER.debug("set league "+field + " on the cache from api")
        self.cache.set_value('league', field, json.dumps(value))

    def get_league(self, field):
        self._LOGGER.debug("get league "+field + " from the cache")
        league = self.cache.get_value('league', field)
        if league:
            return json.loads(league.decode('utf-8'))
        return None

    def set_league_id(self, field, value):
        self._LOGGER.debug("table for reference " + field + " and " + str(value))
        self.cache.set_value("league-id", field, json.dumps(value))

    def get_league_id(self, field):
        self._LOGGER.debug("get id from league name " + field)
        league_id = self.cache.get_value('league-id', field)
        if league_id:
            return str(json.loads(league_id.decode('utf-8')))
        return None

    def set_team(self, field, value):
        self._LOGGER.debug("set team " + field + " on the cache from api")
        self.cache.set_value('team', field, json.dumps(value))

    def get_team(self, field):
        self._LOGGER.debug("get team " + field + " from the cache")
        team = self.cache.get_value('team', field)
        if team:
            return json.loads(team.decode('utf-8'))
        return None

    def set_team_id(self, field, value):
        self._LOGGER.debug("table for reference " + field + " and " + str(value))
        self.cache.set_value("team-id", field, json.dumps(value))

    def get_team_id(self, field):
        self._LOGGER.debug("get id from team name " + field)
        team_id = self.cache.get_value('team-id', field)
        if team_id:
            return str(json.loads(team_id.decode('utf-8')))
        return None

    def set_team_id_leagues(self, field, value):
        self._LOGGER.debug("set list of team ids for " + field + " on the cache from api")
        self.cache.set_value('league-team-ids', field, json.dumps(value))

    def get_team_id_leagues(self, field):
        self._LOGGER.debug("get list of team ids for " + field + " from the cache")
        list_teams_id = self.cache.get_value('league-team-id', field)
        if list_teams_id:
            return json.loads(list_teams_id.decode('utf-8'))
        return None

    def get_all_team_ids(self, value):
        self._LOGGER.debug("get all list of " + value + " from the cache")
        return self.cache.get_all(value)

    def set_team_leagues(self, field, value):
        self._LOGGER.debug("set list of teams for " + field + " on the cache from api")
        self.cache.set_value('league-teams', field, json.dumps(value))

    def get_team_leagues(self, field):
        self._LOGGER.debug("get list of teams for " + field + " from the cache")
        list_teams = self.cache.get_value('league-teams', field)
        if list_teams:
            return json.loads(list_teams.decode('utf-8'))
        return None

    def set_standing(self, field, value):
        self._LOGGER.debug("set standing " + field + " on cache")
        self.cache.set_value("standing-id", field, json.dumps(value))

    def get_standing(self, field):
        self._LOGGER.debug("get stading from id league " + field + " on the cache")
        standing_id = self.cache.get_value('standing-id', field)
        if standing_id:
            return json.loads(standing_id.decode('utf-8'))
        return None
