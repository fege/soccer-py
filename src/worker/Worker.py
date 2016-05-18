from manager.ApiManager import ApiManager

class Worker():
    """ 
    Class that generates stuff
    """

    def __init__(self):
	self.api = ApiManager()

    def print_standing(self, id):
	self.id = id
	for t in self.api.get_league_table(self.id)['standing']:
	    if len(self.api.get_team(t['teamId'])['name']) < 16:
		print(str(t['rank'])+"\t"+self.api.get_team(t['teamId'])['name']+"\t\t"+str(t['points'])+"\t"+str(t['goalDifference'])+"\t"+str(t['playedGames']))
	    else:
                print(str(t['rank'])+"\t"+self.api.get_team(t['teamId'])['name']+"\t"+str(t['points'])+"\t"+str(t['goalDifference'])+"\t"+str(t['playedGames']))
