import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate

positions = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']


def create_team_table(_file_location, _file_name):
    PS = open(_file_location + _file_name, 'r')
    soup = BeautifulSoup(PS, 'lxml')
    tables = soup.find_all('table')[0]
    df = pd.read_html(str(tables))

    _team_table = df[3] # from troubleshooting the third table is the team table
    _team_table = _team_table.drop([5, 10], axis=1).drop([0, 12], axis=0) # remove useless rows and columns
    _team_table = _team_table.dropna(subset=[1]) # drop the IR column if PLAYER value is nan

    # fix a couple column header labels
    _team_table[2][1] = 'POS'
    _team_table[1][1] = 'PLAYER'
    _team_table[2][13] = 'POS'

    _team_table.columns = _team_table.iloc[0] # make 1st row the column headers
    _team_table = _team_table.drop([1]).reset_index(drop=True) # drop 1st row (now column headers) and reindex

    team_table = add_position_row(_team_table)

    return team_table

def add_position_row(table):

    for pos in positions:
        #print(pos)
        # This could be a problem: ValueError: cannot index with vector containing NA / NaN values
        # Try Except will not work. Maybe remove index if not filled
        pos_true = table.index[table['PLAYER'].str.contains('\xa0' + pos)].values
        #print(pos_true)
        table['POS'][pos_true] = pos

    return table

def print_table(table):
    table_str = tabulate(table, headers='keys', tablefmt='psql')
    print(table_str)

if __name__ == '__main__':
    file_location = '..\\offline_webpages\\'
    file_name = 'front_page_source'

    team_table = create_team_table(file_location, file_name)

    print_table(team_table)