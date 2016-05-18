from manager.ApiManager import ApiManager
import logging
import logging.config
logging.config.fileConfig("logging.conf")

class Worker():
    """ 
    Class that generates stuff
    """

    _LOGGER = logging.getLogger('WORKER')

    def __init__(self):
	self.api = ApiManager()

    def print_standing(self, id):
	self.id = id
	standing = self.api.get_league_table(self.id)
	self._LOGGER.debug("Output standing for "+standing['leagueCaption'])
	for t in standing['standing']:
	    if len(self.api.get_team(t['teamId'])['name']) < 16:
		print(str(t['rank'])+"\t"+self.api.get_team(t['teamId'])['name']+"\t\t"+str(t['points'])+"\t"+str(t['goalDifference'])+"\t"+str(t['playedGames']))
	    else:
                print(str(t['rank'])+"\t"+self.api.get_team(t['teamId'])['name']+"\t"+str(t['points'])+"\t"+str(t['goalDifference'])+"\t"+str(t['playedGames']))
