from manager.ApiManager import ApiManager
from worker.Worker import Worker
import pprint

if __name__ == '__main__':
    api = ApiManager()
    pprint.pprint(api.get_season_leagues('2016'))
    print("2015")
    pprint.pprint(api.get_season_leagues('2015'))
    print("-------------------------")
    pprint.pprint(api.get_league_table('398'))
    print("-------------------------")
    pprint.pprint(api.get_team('66'))
    worker = Worker()
    print("-------------------------")
    print(worker.print_standing(398))
