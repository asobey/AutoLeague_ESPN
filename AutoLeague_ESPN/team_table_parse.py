import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import re

POSITIONS = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']

def print_table(table):
    table_str = tabulate(table, headers='keys', tablefmt='psql')
    print(table_str)


def create_team_table(f_location, f_name):
    _PS = open(f_location + f_name, 'r')

    return update_team_table(_PS)


def update_team_table(PS):
    _soup = BeautifulSoup(PS, 'lxml')  # Using BS4 to parse
    _table_soup = _soup.find_all('table')[0]  # Finding the table element in the soup
    _df = pd.read_html(str(_table_soup))  # Making the soup table element into a pandas df
    _team_table = _df[3]  # From troubleshooting the third table is the team table

    #print(tabulate(_team_table, headers='keys', tablefmt='psql'))  # DEBUG

    _team_table = _team_table.fillna('--')  # Fill nan values will -- makes them able to index of of later

    if len(_team_table.columns) == 16:
        raise Exception('full table not loaded')

    _team_table[3][1, 13] = 'POS'  # need to set this early so nan value does not become index
    _team_table = _team_table.drop([2, 6, 11], axis=1).drop([0, 12], axis=0)

    # fix a couple column header labels
    _team_table[1][1] = 'PLAYER'

    # MAKE 1ST ROW COLUMN HEADERS AND DROP 1ST ROW
    _team_table.columns = _team_table.iloc[0]  # make 1st row the column headers
    _team_table = _team_table.drop([1]).reset_index(drop=True)  # drop 1st row (now column headers) and reindex

    for col in _team_table:
        _team_table[col][:9] = pd.to_numeric(_team_table[col][:9], errors='ignore')
        _team_table[col][11:] = pd.to_numeric(_team_table[col][11:], errors='ignore')

    # REMOVE TABS Â
    _team_table = _team_table.replace('Â', '', regex=True)

    _team_table = add_position_col(_team_table)

    _team_table = add_player_id(_team_table, _table_soup)

    team_table_out = add_here_col(_team_table)

    return team_table_out


def add_player_id(team_table, table_soup):
    table_line = str(table_soup.find_all("td", {"class": "playertablePlayerName"}))
    player_ids = list(map(int, re.findall('playername_(\d+)', table_line)))

    # The extra '--' at the end and the [:17] are to resolve having or not having an IR spot
    player_ids_insert = (player_ids[:10] + ['ID'] + player_ids[10:] + ['--'] + ['--'] + ['--'] + ['--'] + ['--'])[:len(team_table)]
    team_table['ID'] = player_ids_insert
    return team_table


def add_position_col(table):
    for pos in POSITIONS:
        pos_true = table.index[table['PLAYER'].str.contains('\xa0' + pos)].values
        table['POS'][pos_true] = pos
    return table


def add_here_col(table):
    #if len(table.index) == 17:
    table['HERE'] = ([0, 1, 2, 3, 4, 5, 6, 14, 7, 8, 'HERE', 9, 10, 11, 12, 13, 14, 15, 16, 17])[:len(table)]
    # elif len(table.index) == 16:
    #     table['HERE'] = ([0, 1, 2, 3, 4, 5, 6, 14, 7, 8, 'HERE', 9, 10, 11, 12, 13])  # not sure which "here" number for IR. maybe not 13
    # elif len(table.index) == 15:
    #     table['HERE'] = ([0, 1, 2, 3, 4, 5, 6, 14, 7, 8, 'HERE', 9, 10, 11, 12])
    # else:
    #     print('table row out of range')
    return table


if __name__ == '__main__':
    file_location = '..\\offline_webpages\\'
    file_name = 'front_page_source'

    team_table = create_team_table(file_location, file_name)

    print_table(team_table)
