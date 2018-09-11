# endpoints for the api:
#   leagueSettings
#   playerInfo --only has 49 players in the list for some reason??
#   scoreboard --json, no value to roster sorting
#   player/news --full text of the news
#   recentActivity --league trading activities
#   leagueSchedules
#   teams --league standing
#   rosterInfo --json, contains position IDs, percent owned, percent started, health status, and some way to tell if you can still move them
#   schedule
#   polls
#   messageboard
#   status --just the current date
#   teams/pendingMoveBatches
#   tweets
#   stories
#   livescoring (doesn’t seem to be working right)
#   boxscore -- looks like this will have all the stats, but will be kinda hard to parse

import requests
from bs4 import BeautifulSoup
import pandas as pd
import yaml
# import numpy as np
import re
from tabulate import tabulate


with open('espn_creds.yaml', 'r') as _private:
    privateData = yaml.load(_private)    # pulls in the person specific data (teamId, cookies, etc)


def create_roster():

    print('----- Moving to Roster Data ------')

    cookies = {
        'espn_s2': privateData['espn_s2'],
        'SWID': privateData['SWID']
    }

    parameters = {
        'leagueId': privateData['leagueid'], 'teamId': privateData['teamid'], 'seasonId': privateData['seasonid']
    }

    r = requests.get("http://games.espn.com/ffl/api/v2/rosterInfo",
                     params=parameters,
                     cookies=cookies)
    roster = r.json()
    rdf = []  # pd.DataFrame(columns=['PlayerID', 'First', 'Last', 'Pos', 'Slot', 'possible slot'])
    temp2 = roster['leagueRosters']['teams'][0]['slots']
    for match in temp2:
        rdf.append([match['player']['playerId'],
                    match['player']['firstName'],
                    match['player']['lastName'],
                    match['player']['defaultPositionId'],  # Player IDs are: 1=QB; 2=RB; 3=WR; 4=TE; 5=K; 16=D/ST
                    match['slotCategoryId'],  # Position IDs are: 0=QB; 2=RB; 3=RB/WR; 4=WR; 6=TE; 23=FLEX; 17=K; 16=D/ST; 20=Bench; 21=IR
                    match['player']['eligibleSlotCategoryIds']])

    table_str = tabulate(rdf, headers='keys', tablefmt='psql')
    return table_str


def add_player_id(team_table, table_soup):
    table_line = str(table_soup.find_all("td", {"class": "playertablePlayerName"}))
    player_ids = list(map(int, re.findall('playername_(\d+)', table_line)))

    # The extra '--' at the end and the [:17] are to resolve having or not having an IR spot
    player_ids_insert = (player_ids[:10] + ['ID'] + player_ids[10:] + ['--'] + ['--'] + ['--'] + ['--'] + ['--'])[:len(team_table)]
    team_table['ID'] = player_ids_insert
    return team_table


def top_waiver(position):
    """this "top" ranking is personal preference. initial setup is based on espn's projection"""

    df = create_waiver(position)
    player = df.nlargest(3, 'Projected')
    print(tabulate(player, headers='keys', tablefmt='psg1'))

    return player


def create_waiver(position='none'):
    """Listing of "position" players on the waiver wire."""

    cookies = {
        'espn_s2': privateData['espn_s2'],
        'SWID': privateData['SWID']
    }

    # slot codes used to get the right page
    slots = {'QB': 0, 'RB': 2, 'RB/WR': 3, 'WR': 4, 'TE': 6, 'D/ST': 16, 'K': 17, 'FLEX': 23}
    slot = slots[position]

    if position == 'none':
        parameters = {'leagueId': privateData['leagueid'], 'teamID': privateData['teamid'],
                      'avail': 1, 'injury': 2, 'context': 'freeagency', 'view': 'overview'}
    else:
        parameters = {'leagueId': privateData['leagueid'], 'teamID': privateData['teamid'],
                      'slotCategoryId': slot, 'avail': 1, 'injury': 2, 'context': 'freeagency',
                      'view': 'overview'}

    df = pd.DataFrame(columns=['Player', 'Opponent', 'Projected', 'OppRank', '%Start', '%Own', '+/-'])

    for si in [0, 50, 100]:
        parameters['startIndex'] = si
        r = requests.get('http://games.espn.com/ffl/freeagency',
                         params=parameters,
                         cookies=cookies)

        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', class_='playerTableTable')
        tdf = pd.read_html(str(table), flavor='bs4')[0]  # returns a list of df's, grab first

        tdf = tdf.iloc[2:, [0, 5, 13, 14, 15, 16, 17]].reset_index(drop=True)  # delete the useless columns
        tdf = add_player_id(tdf, soup)
        tdf.columns = ['Player', 'Opponent', 'Projected', 'OppRank', '%Start', '%Own', '+/-', 'PlayerID']
        df = df.append(tdf, ignore_index=True, sort=False)  # !!!! non-concatenation axis is not aligned. remove the "sort=false" to troubleshoot

    df = df.query('Projected != "--"')

    df['Projected'] = df['Projected'].fillna(0).astype('float')
    df['Player'] = df['Player'].str.split(',').str[0]  # keep just player name
    # print(tabulate(tdf, headers='keys', tablefmt='psg1'))


    return df


def create_leaders():

    cookies = {
        'espn_s2': privateData['espn_s2'],
        'SWID': privateData['SWID']
    }

    r = requests.get('http://games.espn.com/ffl/leaders',
                     params={'leagueId': 413011, 'seasonId': 2018,
                             'scoringPeriodId': 1,
                             'slotCategoryId': 0},
                     cookies=cookies)

    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', class_='playerTableTable')
    tdf = pd.read_html(str(table), flavor='bs4')[0]  # returns a list of df's, grab first

    print(tabulate(tdf, headers='keys', tablefmt='psg1'))

    tdf = tdf.drop([1, 3, 4, 7, 12, 16, 21, 25], axis=1)  # remove useless rows and columns

    print(tabulate(tdf, headers='keys', tablefmt='psg1'))

    tdf = tdf.drop([0]).reset_index(drop=True)  # drop 1st row (now column headers) and reindex
    tdf.columns = tdf.iloc[0]  # make 1st row the column headers
    tdf = tdf.drop([0]).reset_index(drop=True)  # drop 1st row (now column headers) and reindex
    # fix column header labels with something like tdf[2][1] = 'POS'
    # consider tdf.dropna(subset=[1]) to drop nan columns?

    table_str = tabulate(tdf, headers='keys', tablefmt='psql')
    # print(table_str)

    return 0


def boxscores():
    parameters = {
        'leagueId': privateData['leagueid'], 'teamId': privateData['teamid'], 'seasonId': privateData['seasonid']
    }

    r = requests.get("http://games.espn.com/ffl/api/v2/rosterInfo",
                     params=parameters)

    # slot codes
    slots = {0: 'QB', 2: 'RB', 4: 'WR', 6: 'TE',
             16: 'D/ST', 17: 'K', 20: 'BE', 23: 'FLEX'}

    # rows will be by player by week
    df = pd.DataFrame(columns=['playerName', 'matchupPeriodId',
                               'slotId', 'position', 'bye', 'appliedStatTotal',
                               'teamAbbrev', 'wonMatchup'])

    for week in range(1, 17):
        for match in range(len(sbs[week]['scoreboard']['matchups'])):
            homeId = sbs[week]['scoreboard']['matchups'][match]['teams'][0]['team']['teamId']
            winner = sbs[week]['scoreboard']['matchups'][match]['winner']

            # loop through home (0) and away (1)
            for team in range(2):
                # boolean for who won this matchup
                winb = False
                if (winner == 'away' and team == 1) or (winner == 'home' and team == 0):
                    winb = True

                # fantasy team info (dict)
                tinfo = bss[week][match]['boxscore']['teams'][team]['team']

                # all players on that team info (array of dicts)
                ps = bss[week][match]['boxscore']['teams'][team]['slots']

                # loop through players
                for k, p in enumerate(ps):
                    # players on bye/injured won't have this entry
                    try:
                        pts = p['currentPeriodRealStats']['appliedStatTotal']
                    except KeyError:
                        pts = 0

                    # there is some messiness in the json so just skip
                    try:
                        # get player's position. this is a bit hacky...
                        pos = p['player']['eligibleSlotCategoryIds']
                        for s in [20, 23]:
                            if pos.count(s) > 0:
                                pos.remove(s)
                        pos = slots[pos[0]]

                        # add it all to the DataFrame
                        df = df.append({'playerName': p['player']['firstName'] + ' ' + p['player']['lastName'],
                                        'matchupPeriodId': week,
                                        'slotId': p['slotCategoryId'],
                                        'position': pos,
                                        'bye': True if p['opponentProTeamId'] == -1 else False,
                                        'appliedStatTotal': pts,
                                        'teamAbbrev': tinfo['teamAbbrev'],
                                        'wonMatchup': winb},
                                       ignore_index=True)
                    except KeyError:
                        continue

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

# temp...copies from sobey's code


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

if __name__ == '__main__':
    # table1 = create_roster()
    # table1 = boxscores()
    # table1 = create_leaders()
    # print(table1)
    top_waiver('QB')


