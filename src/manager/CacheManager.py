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
        self.cache.set_value("league-id", field, value)

    def get_league_id(self, field):
        self._LOGGER.debug("get id from league name" + field)
        league_id = self.cache.get_value('league-id', field)
        if league_id:
            return str(json.loads(league_id.decode('utf-8')))
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
