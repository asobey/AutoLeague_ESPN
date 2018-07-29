from espnff import League
league_id = 413011  # random league that works: 125878
year = 2017
league = League(league_id, year)
print(league.teams)

team1 = league.teams[0]
print(team1.points_for)
