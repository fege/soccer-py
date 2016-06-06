from manager.ApiManager import ApiManager
from pprint import pprint

if __name__ == '__main__':
    api = ApiManager()
    #pprint(api.get_season_leagues('2016'))
    #print("2015")
    #pprint(api.get_season_leagues('2015'))
    print("-------------------------")
    #pprint(api.get_league('Premier League 2015/16'))
    print("-------------------------")
    #pprint(api.get_team('66'))
    print("-------------------------")
    pprint(api.get_league('Serie A 2015/16'))
    #pprint(api.get_teams_league('Premier League 2015/16'))
    pprint(api.get_teams_league('Serie A 2015/16'))
    #standing = api.get_league_table('Premier League 2015/16')
    #for t in standing['standing']:
    #    if len(t["team"]) < 8:
    #        print(
    #            t["team"] + "\t\t\t" + str(t["points"]) + "\t" + str(t['goalDifference']) + "\t" + str(t['playedGames']))
    #    elif len(t["team"]) > 12:
    #        print(t["team"] + "\t" + str(t["points"]) + "\t" + str(t['goalDifference']) + "\t" + str(t['playedGames']))
    #    else:
    #        print(t["team"] + "\t\t" + str(t["points"]) + "\t" + str(t['goalDifference']) + "\t" + str(t['playedGames']))
