from espnff import League, Team

league_id = 413011  # random league that works: 125878
year = 2017

league = League(league_id, year)

for team in league.teams:
    print(team)

#for team in league.teams:
#    print(team.owner)


team1 = league.teams[0]
print(team1.points_for)
print(team1.schedule)
print(type(team1))

print(team1.get_roster(week=5))
