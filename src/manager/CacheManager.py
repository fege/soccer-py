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
