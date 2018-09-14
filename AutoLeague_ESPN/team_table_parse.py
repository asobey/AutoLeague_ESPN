import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import os

POSITIONS = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']

def print_table(table):
    table_str = tabulate(table, headers='keys', tablefmt='psql')
    print(table_str)


def create_team_table(f_location, f_name):
    source_path = os.path.join(f_location, f_name)
    print(f'CWD: {os.getcwd()}')
    print(f'Opening page source from Source Path: {source_path}')
    _PS = open(source_path, 'r')
    return update_team_table(_PS)


def update_team_table(PS):
    _soup = BeautifulSoup(PS, 'lxml')  # Using BS4 to parse
    _table_soup = _soup.find_all('table')[0]  # Finding the table element in the soup
    _df = pd.read_html(str(_table_soup))  # Making the soup table element into a pandas df
    _team_table = _df[3]  # From troubleshooting the third table is the team table

    #print(tabulate(_team_table, headers='keys', tablefmt='psql'))  # DEBUG

    _team_table = _team_table.fillna('--')  # Fill nan values with -- makes them able to index of of later

    if len(_team_table.columns) != 17:
        print(f'full table not loaded, {len(_team_table.columns)} columns exist')  # Debug
        #raise Exception(f'full table not loaded, {len(_team_table.columns)} columns exist')

    _team_table[3][1, 13] = 'POS'  # need to set this early so nan value does not become index
    _team_table = _team_table.drop([2, 6, 11], axis=1).drop([0, 12, 13], axis=0)

    _team_table.loc[1, 1] = 'PLAYER'
    # MAKE 1ST ROW COLUMN HEADERS AND DROP 1ST ROW
    _team_table.columns = _team_table.iloc[0]  # make 1st row the column headers
    _team_table = _team_table.drop([1]).reset_index(drop=True)  # drop 1st row (now column headers) and reindex

    # Change numeric value to numbers instead of strings. Does not affect non-numbers
    filled_rows = []
    for i in _team_table.index:
        if _team_table['OPP'][i] != '--':
            filled_rows.append(i)
    # print(f'Filled Row: {filled_rows}')  # DEBUG
    numeric_cols = ['PRK', 'PTS', 'AVG', 'PROJ', '%ST', '%OWN', '+/-']
    for col in numeric_cols:
        _team_table[col] = pd.to_numeric(_team_table[col][filled_rows], errors='coerce')
    # print(type(_team_table['PRK'][5]))  #DEBUG

    # REMOVE TABS Â
    _team_table = _team_table.replace('Â', '', regex=True)

    _team_table = add_position_col(_team_table)

    _team_table = add_player_id(_team_table, _table_soup)

    _team_table = add_here_col(_team_table)

    _team_table = _team_table.fillna('--')  # Again, fill nan values with -- makes them able to index of of later

    col_order = ['HERE','SLOT', 'POS', 'ID', 'PLAYER', 'PTS', 'AVG',
       'LAST', 'PROJ', '%ST', '%OWN', '+/-', 'OPRK', 'OPP', 'PRK', 'STATUS ET']  # Changing col order for user
    team_table_out = _team_table[col_order]

    return team_table_out


def add_player_id(team_table, table_soup):
    """This function searches the BS4 soup for each players ID then adds it"""
    table_line = str(table_soup.find_all("td", {"class": "playertablePlayerName"}))
    player_ids = list(map(int, re.findall('playername_(\d+)', table_line)))
    player_ids_insert = ['--'] * len(team_table)  # Start by filling all rows will '--'
    team_table['ID'] = player_ids_insert
    for i in team_table.index:
        if team_table['POS'][i] != '--':
            if len(player_ids) > 0:
                team_table['ID'][i] = player_ids[0]
                player_ids.pop(0)
    return team_table


def add_position_col(table):
    """This function finds the position of each player by parsing the 'PLAYER' column, then adds a 'POS' column with
    that value."""
    for pos in POSITIONS:
        pos_true = table.index[table['PLAYER'].str.contains('\xa0' + pos, na=False)].values
        table.loc[pos_true, 'POS'] = pos  # This is how to correctly set value in df
    return table


def add_here_col(table):
    """This function simply adds a 'HERE' column. HERE is the slot position recognized by the weddriver when moving
    players around."""
    table['HERE'] = ([0, 1, 2, 3, 4, 5, 6, 14, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18])[:len(table)]
    return table


if __name__ == '__main__':
    file_location = '..\\offline_webpages\\'
    file_name = 'front_page_source'

    team_table = create_team_table(file_location, file_name) # read table from source

    print_table(team_table)
