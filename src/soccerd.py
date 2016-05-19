from manager.ApiManager import ApiManager
from pprint import pprint

if __name__ == '__main__':
    api = ApiManager()
    pprint(api.get_season_leagues('2016'))
    print("2015")
    pprint(api.get_season_leagues('2015'))
    print("-------------------------")
    pprint(api.get_league_table('398'))
    print("-------------------------")
    pprint(api.get_team('66'))
    print("-------------------------")
    standing = api.get_league_table(398)
    for t in standing['standing']:
        if len(api.get_team(t['teamId'])['name']) < 16:
            print(
                str(t['rank']) + "\t" + api.get_team(t['teamId'])['name'] + "\t\t" + str(t['points']) + "\t" + str(
                    t['goalDifference']) + "\t" + str(t['playedGames']))
        else:
            print(str(t['rank']) + "\t" + api.get_team(t['teamId'])['name'] + "\t" + str(t['points']) + "\t" + str(
                t['goalDifference']) + "\t" + str(t['playedGames']))
