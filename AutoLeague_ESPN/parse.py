import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import os


class Parse(object):

    def __init__(self):
        self.POSITIONS = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']

    def team_table(self, page_source=None):
        if page_source != None:
            self.team = self.table(page_source)
        else:
            try:
                self.team = self.table_from_file()
            except NotImplementedError:
                print('Neither file nor page_source available to make table')

    def print_table(self):
        """Simply prints table in nice format"""
        print(tabulate(self.team_table, headers='keys', tablefmt='psql'))

    def table_from_file(self, private_data):
        """Create table from a offline source file."""
        source_path = os.path.join(private_data['source_file_location'], private_data['source_file_name'])
        print(f'CWD: {os.getcwd()}')
        print(f'Opening page source from Source Path: {source_path}')
        _PS = open(source_path, 'r')
        return self.table_from_source(_PS)

    def table_from_source(self, page_source):
        """Create team table."""
        sourse_soup = BeautifulSoup(page_source, 'lxml')  # Using BS4 to parse
        _table_soup = sourse_soup.find_all('table')[0]  # Finding the table element in the soup
        _df = pd.read_html(str(_table_soup))  # Making the soup table element into a pandas df
        team_table = _df[3]  # From troubleshooting the third table is the team table
        # Check if table loaded after login
        if len(team_table.columns) != 17:
            raise Exception(f'full table not loaded, {len(team_table.columns)} columns exist')
        # Start of cleaning up the table
        team_table = team_table.fillna('--')  # Fill nan values with -- makes them able to index of of later
        team_table[3][1, 13] = 'POS'  # need to set this early so nan value does not become index
        team_table.loc[1, 1] = 'PLAYER'
        team_table = team_table.drop([2, 6, 11], axis=1).drop([0, 12, 13], axis=0)
        # MAKE 1ST ROW COLUMN HEADERS AND DROP 1ST ROW
        team_table.columns = team_table.iloc[0]  # make 1st row the column headers
        team_table = team_table.drop([1]).reset_index(drop=True)  # drop 1st row (now column headers) and reindex
        # Change numeric value to numbers instead of strings. Does not affect non-numbers
        filled_rows = []
        for i in team_table.index:
            if team_table['OPP'][i] != '--':
                filled_rows.append(i)
        numeric_cols = ['PRK', 'PTS', 'AVG', 'PROJ', '%ST', '%OWN', '+/-']
        for col in numeric_cols:
            team_table[col] = pd.to_numeric(team_table[col][filled_rows], errors='coerce')
        # REMOVE TABS Â
        team_table = team_table.replace('Â', '', regex=True)
        # Add column methods 3X
        team_table = self.add_position_col(team_table)
        team_table = self.add_player_id(team_table, _table_soup)
        team_table = self.add_here_col(team_table)

        team_table = team_table.fillna('--')  # Again, fill nan values with -- makes them able to index of of later
        col_order = ['HERE','SLOT', 'POS', 'ID', 'PLAYER', 'PTS', 'AVG', 'LAST', 'PROJ', '%ST', '%OWN',
                     '+/-', 'OPRK', 'OPP', 'PRK', 'STATUS ET']  # Changing col order for user
        return team_table[col_order]

    @staticmethod
    def add_player_id(self, team_table, table_soup):
        """This function searches the BS4 soup for each players ID then adds it"""
        table_line = str(table_soup.find_all("td", {"class": "playertablePlayerName"}))
        player_ids = list(map(int, re.findall('playername_(\d+)', table_line)))
        player_ids_insert = ['--'] * len(team_table)  # Start by filling all rows will '--'
        team_table['ID'] = player_ids_insert
        for i in team_table.index:
            if team_table['POS'][i] != '--':
                if len(player_ids) > 0:
                    team_table.loc[i, 'ID'] = player_ids[0]
                    player_ids.pop(0)
        return team_table

    @staticmethod
    def add_position_col(self, table):
        """This function finds the position of each player by parsing the 'PLAYER' column, then adds a 'POS' column with
        that value."""
        for pos in self.POSITIONS:
            pos_true = table.index[table['PLAYER'].str.contains('\xa0' + pos, na=False)].values
            table.loc[pos_true, 'POS'] = pos  # This is how to correctly set value in df
        return table

    def add_here_col(self, table):
        """This function simply adds a 'HERE' column. HERE is the slot position recognized by the weddriver when moving
        players around."""
        table['HERE'] = ([0, 1, 2, 3, 4, 5, 6, 14, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18])[:len(table)]
        return table


if __name__ == '__main__':
    import yaml
    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        pd = yaml.load(_private)

    Parse.table_from_file(pd)  # read table from source

    Parse.print_table()
