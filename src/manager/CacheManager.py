import logging
import logging.config
logging.config.fileConfig("logging.conf")


class CacheManager():
    """
    Class that interact with Driver
    """
    _LOGGER = logging.getLogger('CACHE_MANAGER')

    def __init__(self):
        resource = "src.storage.RedisDriver"
        resource_mod = __import__(resource, globals(), locals(), ['RedisDriver'])
        cache = getattr(resource_mod, 'RedisDriver')
        self.cache = cache()

    def set_league(self,field, value):
        self._LOGGER.debug("set league "+field+ " on the cache")
        self.cache.set_value('league', field, value)

    def get_league(self, field):
        self._LOGGER.debug("get league "+field+ " from the cache")
        return self.cache.get_value('league', field)
