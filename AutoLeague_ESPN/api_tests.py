# endpoints for the api:
#   leagueSettings
#   playerInfo
#   scoreboard --json
#   player/news
#   recentActivity
#   leagueSchedules
#   teams
#   rosterInfo --json
#   schedule
#   polls
#   messageboard
#   status
#   teams/pendingMoveBatches
#   tweets
#   stories
#   livescoring (doesn’t seem to be working right)
#   boxscore

import requests
from bs4 import BeautifulSoup
import pandas as pd
import yaml
import numpy as np
from tabulate import tabulate
import re

with open('espn_creds.yaml', 'r') as _private:
    privateData = yaml.load(_private)

# scores = {}
# for week in range(1, 17):
#     r = requests.get('http://games.espn.com/ffl/api/v2/scoreboard',
#                      params={'leagueId': 413011, 'seasonId': 2018, 'matchupPeriodId': week})
#     scores[week] = r.json()
#
# df = []
# for key in scores:
#     temp = scores[key]['scoreboard']['matchups']
#     for match in temp:
#         df.append([key,
#                    match['teams'][0]['team']['teamAbbrev'],
#                    match['teams'][1]['team']['teamAbbrev'],
#                    match['teams'][0]['score'],
#                    match['teams'][1]['score']])
#
# df = pd.DataFrame(df, columns=['Week', 'HomeAbbrev', 'AwayAbbrev', 'HomeScore', 'AwayScore'])
# df.head()
#
#
# table_str = tabulate(df, headers='keys', tablefmt='psql')
# print(table_str)

print('----- Moving to Roster Data ------')

cookies = {
    'espn_s2': privateData['espn_s2'],
    'SWID': privateData['SWID']
}

parameters = {
    'leagueId': 413011, 'teamId': 10, 'seasonId': 2018
}

r = requests.get("http://games.espn.com/ffl/api/v2/rosterInfo",
                 params=parameters,
                 cookies=cookies)
roster = r.json()
rdf = []
temp2 = roster['leagueRosters']['teams'][0]['slots']
i = 1
for match in temp2:
    rdf.append([i,
                match['player']['firstName'],
                match['player']['lastName']])
    i = i+1

table_str = tabulate(rdf, headers='keys', tablefmt='psql')
print(table_str)

print('---------- Moving on to the Leader Board ------------')

leaders = {}
r = requests.get('http://games.espn.com/ffl/leaders',
                 params={'leagueId': 413011, 'seasonId': 2018,
                         'scoringPeriodId': 1,
                         'slotCategoryId': 0},
                 cookies=cookies)

soup = BeautifulSoup(r.content, 'html.parser')
table = soup.find('table', class_='playerTableTable')
tdf = pd.read_html(str(table), flavor='bs4')[0]  # returns a list of df's, grab first


tdf = tdf.drop([1,3,4,9,13,18,22], axis=1) # remove useless rows and columns

tdf = tdf.drop([0]).reset_index(drop=True) # drop 1st row (now column headers) and reindex
tdf.columns = tdf.iloc[0] # make 1st row the column headers
tdf = tdf.drop([0]).reset_index(drop=True) # drop 1st row (now column headers) and reindex


table_str = tabulate(tdf, headers='keys', tablefmt='psql')
print(table_str)

# df = pd.DataFrame(df, columns=['one', 'two', 'three', 'four'])

# positions = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']



# def create_team_table(file_location, file_name):
#     _PS = open(file_location + file_name, 'r')
#     _soup = BeautifulSoup(_PS, 'lxml')
#     _PS.close()
#     table_soup = _soup.find_all('table')[0]
#
#     df = pd.read_html(str(table_soup))
#
#     _team_table = df[3] # from troubleshooting the third table is the team table
#     _team_table = _team_table.drop([5, 10], axis=1).drop([0, 12], axis=0) # remove useless rows and columns
#     _team_table = _team_table.dropna(subset=[1]) # drop the IR column if PLAYER value is nan
#
#     # fix a couple column header labels
#     _team_table[2][1] = 'POS'
#     _team_table[1][1] = 'PLAYER'
#     _team_table[2][13] = 'POS'
#
#     _team_table.columns = _team_table.iloc[0] # make 1st row the column headers
#     _team_table = _team_table.drop([1]).reset_index(drop=True) # drop 1st row (now column headers) and reindex
#
#     for col in _team_table:
#         _team_table[col][:9] = pd.to_numeric(_team_table[col][:9], errors='ignore')
#         _team_table[col][11:] = pd.to_numeric(_team_table[col][11:], errors='ignore')
#
#     _team_table = add_position_col(_team_table)
#
#     _team_table = add_player_id(_team_table, table_soup)
#
#
#     team_table_out = add_here_col(_team_table)
#
#     return team_table_out
#
# def add_player_id(team_table, table_soup):
#
#     table_line = str(table_soup.find_all("td", {"class": "playertablePlayerName"}))
#     player_ids = list(map(int, re.findall('playername_(\d+)', table_line)))
#     player_ids_insert = player_ids[:9] + ['ID'] + player_ids[9:]
#     team_table['ID'] = player_ids_insert
#     return team_table
#
#
# def add_position_col(table):
#     for pos in positions:
#         #print(pos)
#         # This could be a problem: ValueError: cannot index with vector containing NA / NaN values
#         # Try Except will not work. Maybe remove index if not filled
#         pos_true = table.index[table['PLAYER'].str.contains('\xa0' + pos)].values
#         #print(pos_true)
#         table['POS'][pos_true] = pos
#     return table
#
#
# def add_here_col(table):
#     if len(table.index)==16:
#         table['HERE'] = ([0,1,2,3,4,5,6,14,7,8,'HERE',9,10,11,12,13]) #not sure which "here" number for IR. maybe not 13
#     elif len(table.index)==15:
#         table['HERE'] = ([0,1,2,3,4,5,6,14,7,8,'HERE',9,10,11,12])
#     else:
#         print('table row out of range')
#     return table
#
#
# def update_team_table(table):
#     """currently takes save_source and create table to update table. This should simplify that"""
#     pass
#
#
# def print_table(table):
#     table_str = tabulate(table, headers='keys', tablefmt='psql')
#     print(table_str)
#
#
# if __name__ == '__main__':
#
#     team_table = create_team_table(file_location, file_name)
#
#     print_table(team_table)