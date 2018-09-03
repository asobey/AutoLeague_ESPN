import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import re

positions = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']

def print_table(table):
    table_str = tabulate(table, headers='keys', tablefmt='psql')
    print(table_str)


def update_team_table(_PS):
    _soup = BeautifulSoup(_PS, 'lxml')
    _table_soup = _soup.find_all('table')[0]

    _df = pd.read_html(str(_table_soup))

    _team_table = _df[3] # from troubleshooting the third table is the team table

    print_table(_team_table)  # DEBUG
    if len(_team_table.keys.values) == 16:
        _team_table = _team_table.drop([3], axis=1)
        print_table(_team_table)  # DEBUG

    _team_table = _team_table.drop([5, 10], axis=1).drop([0, 12], axis=0) # remove useless rows and columns
    _team_table = _team_table.dropna(subset=[1]) # drop the IR column if PLAYER value is nan

    # fix a couple column header labels
    _team_table[2][1] = 'POS'
    _team_table[1][1] = 'PLAYER'
    print('_team_table[2][13]: ' + str(_team_table[2][13]))  # DEBUG
    _team_table[2][13] = 'POS'
    print('_team_table[2][13] fix: ' + str(_team_table[2][13]))  # DEBUG

    _team_table.columns = _team_table.iloc[0] # make 1st row the column headers
    _team_table = _team_table.drop([1]).reset_index(drop=True) # drop 1st row (now column headers) and reindex

    for col in _team_table:
        _team_table[col][:9] = pd.to_numeric(_team_table[col][:9], errors='ignore')
        _team_table[col][11:] = pd.to_numeric(_team_table[col][11:], errors='ignore')

    _team_table = add_position_col(_team_table)

    _team_table = add_player_id(_team_table, _table_soup)

    team_table_out = add_here_col(_team_table)

    return team_table_out

def create_team_table_old(file_location, file_name):  # made new create_team_table but don't want to get rid of this just yet
    _PS = open(file_location + file_name, 'r')
    print(_PS)
    _soup = BeautifulSoup(_PS, 'lxml')
    _PS.close()
    table_soup = _soup.find_all('table')[0]

    df = pd.read_html(str(table_soup))

    _team_table = df[3] # from troubleshooting the third table is the team table
    _team_table = _team_table.drop([5, 10], axis=1).drop([0, 12], axis=0) # remove useless rows and columns
    _team_table = _team_table.dropna(subset=[1]) # drop the IR column if PLAYER value is nan

    # fix a couple column header labels
    _team_table[2][1] = 'POS'
    _team_table[1][1] = 'PLAYER'
    _team_table[2][13] = 'POS'

    _team_table.columns = _team_table.iloc[0] # make 1st row the column headers
    _team_table = _team_table.drop([1]).reset_index(drop=True) # drop 1st row (now column headers) and reindex

    for col in _team_table:
        _team_table[col][:9] = pd.to_numeric(_team_table[col][:9], errors='ignore')
        _team_table[col][11:] = pd.to_numeric(_team_table[col][11:], errors='ignore')

    _team_table = add_position_col(_team_table)

    _team_table = add_player_id(_team_table, table_soup)

    team_table_out = add_here_col(_team_table)

    return team_table_out


def create_team_table(file_location, file_name):
    _PS = open(file_location + file_name, 'r')

    return update_team_table(_PS)

def add_player_id(team_table, table_soup):

    table_line = str(table_soup.find_all("td", {"class": "playertablePlayerName"}))
    player_ids = list(map(int, re.findall('playername_(\d+)', table_line)))
    player_ids_insert = player_ids[:9] + ['ID'] + player_ids[9:]
    team_table['ID'] = player_ids_insert
    return team_table


def add_position_col(table):
    for pos in positions:
        #print(pos)
        # This could be a problem: ValueError: cannot index with vector containing NA / NaN values
        # Try Except will not work. Maybe remove index if not filled
        pos_true = table.index[table['PLAYER'].str.contains('\xa0' + pos)].values
        #print(pos_true)
        table['POS'][pos_true] = pos
    return table


def add_here_col(table):
    if len(table.index)==16:
        table['HERE'] = ([0,1,2,3,4,5,6,14,7,8,'HERE',9,10,11,12,13]) #not sure which "here" number for IR. maybe not 13
    elif len(table.index)==15:
        table['HERE'] = ([0,1,2,3,4,5,6,14,7,8,'HERE',9,10,11,12])
    else:
        print('table row out of range')
    return table


if __name__ == '__main__':
    file_location = '..\\offline_webpages\\'
    file_name = 'front_page_source'

    team_table = create_team_table2(file_location, file_name)

    print_table(team_table)
