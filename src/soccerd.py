from manager.ApiManager import ApiManager

if __name__ == '__main__':
    api = ApiManager()
    print(api.get_season_leagues('2016'))
    print("2015")
    print(api.get_season_leagues('2015'))
