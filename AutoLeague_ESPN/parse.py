import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import os


class Parse(object):

    def __init__(self):
        self.POSITIONS = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']
        self.WAIVER_POS = ['QB', 'RB', 'RB/WR', 'WR', 'TE', 'FLEX', 'K', 'D/ST', 'ALL']
        self.team = pd.DataFrame
        self.waiver = {}

    def team_table(self, page_source=None):
        if page_source is not None:
            print('Using table from file.')
            self.table_from_source(page_source)
        else:
            try:
                self.table_from_source(page_source)
            except NotImplementedError:
                print('Neither file nor page_source available to make table')

    def print_table(self, table):
        """Simply prints table in nice format"""
        print(tabulate(table, headers='keys', tablefmt='psql'))

    def table_from_file(self, private_data):
        """Create table from a offline source file."""
        source_path = os.path.join(private_data['source_file_location'], private_data['source_file_name'])
        print(f'CWD: {os.getcwd()}')
        print(f'Opening page source from Source Path: {source_path}')
        _PS = open(source_path, 'r')
        self.table_from_source(_PS)

    def table_from_source(self, page_source):
        """Create team table."""
        source_soup = BeautifulSoup(page_source, 'lxml')  # Using BS4 to parse
        _table_soup = source_soup.find_all('table')[0]  # Finding the table element in the soup
        _df = pd.read_html(str(_table_soup))  # Making the soup table element into a pandas df
        team_table = _df[3]  # From troubleshooting the third table is the team table
        # Check if table loaded after login
        if len(team_table.columns) != 17:
            raise Exception(f'full table not loaded, {len(team_table.columns)} columns exist')
        # Start of cleaning up the table
        team_table = team_table.fillna('--')  # Fill nan values with -- makes them able to index of of later
        team_table.loc[1, 3] = 'POS'  # need to set this early so nan value does not become index
        team_table.loc[1, 1] = 'PLAYER'
        team_table = team_table.drop([2, 6, 11], axis=1)  # drops the unused columns
        # MAKE 1ST ROW COLUMN HEADERS AND DROP 1ST ROW
        team_table.columns = team_table.iloc[1]  # make 2nd row the column headers
        team_table = team_table[team_table.PROJ != 'PROJ']  # Removes the second header row
        team_table = team_table[team_table.PLAYER != '--']  # removes any unused roster slots from the table
        team_table = team_table.reset_index(drop=True)  # reindex
        team_table.PROJ.loc[team_table.PROJ == '--'] = 0
        # print(tabulate(team_table, headers='keys', tablefmt='psg1'))
        numeric_cols = ['PRK', 'PTS', 'AVG', 'PROJ', '%ST', '%OWN', '+/-']
        team_table[numeric_cols] = team_table[numeric_cols].apply(pd.to_numeric, errors='coerce')
        # REMOVE TABS Â
        team_table = team_table.replace('Â', '', regex=True)
        # Add column methods 3X
        team_table = self.add_position_col(team_table)
        team_table = self.add_player_id(team_table, _table_soup)
        team_table = self.add_here_col(team_table)

        team_table = team_table.fillna('--')  # Again, fill nan values with -- makes them able to index of of later
        col_order = ['HERE', 'SLOT', 'POS', 'ID', 'PLAYER', 'PTS', 'AVG', 'LAST', 'PROJ', '%ST', '%OWN',
                     '+/-', 'OPRK', 'OPP', 'PRK', 'STATUS ET']  # Changing col order for user
        self.team = team_table[col_order]

    def waiver_table_from_source(self, waiver_source_dict):
        """Listing of "position" playerIds on the waiver. Excludes players not playing this week (BYE or real life FA)"""

        df = pd.DataFrame()

        for start_index in range(0, len(waiver_source_dict)):  #
            try:  # fix this as it loses out on the last page i think
                print('Parsing waiver page', start_index, '...')
                soup = BeautifulSoup(waiver_source_dict[start_index].content, 'html.parser')
                table = soup.find('table', class_='playerTableTable')
                tdf = pd.read_html(str(table), flavor='bs4')[0]  # returns a list of df's, grab first
                tdf = tdf.iloc[2:, [0, 2, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16,
                                    17]]  # Identify the columns you want to keep by deleting the useless columns
                table_line = str(soup.find_all("td", {"class": "playertablePlayerName"}))
                tdf['ID'] = list(map(int, re.findall('playername_(\d+)', table_line)))  # add the player ID
                # print(tabulate(tdf, headers='keys', tablefmt='psg1'))
                df = df.append(tdf, ignore_index=True,
                               sort=False)
                # !!!! non-concatenation axis is not aligned. remove the "sort=false" to troubleshoot
            except ValueError:
                print('Looks like your cookies are not working properly')
                raise
            except:  # need to fix this to clarify what the error is that I'm looking for
                print('You ran into the last page of something, but that is ok for now')
                break
        # print(tabulate(df, headers='keys', tablefmt='psg1'))
        df.columns = ['Player', 'Waiver Day', 'Team', 'Game Time', 'PRK', 'PTS', 'AVG', 'LAST', 'PROJ', 'OPRK', '%ST',
                      '%OWN', '+/-', 'ID']
        df['POS'] = df['Player'].str.split(',').str[1]  # parse out the position, part 1
        # if df['POS'].str.split().str[2] it contains the injury status, i think (Q, O, etc.)
        df['POS'] = df['POS'].str.split().str[1]  # parse out the position (might be a better way of doing this)
        df['Player'] = df['Player'].str.split(',').str[0]  # keep just player name
        df.query('PROJ != "--"', inplace=True)  # Delete the players with "--", as these are not playing this week
        df['PROJ'] = df['PROJ'].fillna(0).astype('float')  #
        col_order = ['Player', 'POS', 'Waiver Day', 'Team', 'Game Time', 'PRK', 'PTS', 'AVG', 'LAST', 'PROJ', 'OPRK',
                     '%ST',
                     '%OWN', '+/-', 'ID']  # Changing col order for user UPDATE!!!!
        self.waiver['ALL'] = df[col_order]  # there is a better way to do this
        # print(tabulate(self.waiver['ALL'], headers='keys', tablefmt='psg1'))

    @staticmethod
    def add_player_id(team_table, table_soup):
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

    def add_position_col(self, table):
        """This function finds the position of each player by parsing the 'PLAYER' column, then adds a 'POS' column with
        that value."""
        for pos in self.POSITIONS:
            pos_true = table.index[table['PLAYER'].str.contains('\xa0' + pos, na=False)].values
            table.loc[pos_true, 'POS'] = pos  # This is how to correctly set value in df
        return table

    @staticmethod
    def add_here_col(table):
        """This function simply adds a 'HERE' column. HERE is the slot position recognized by the weddriver when moving
        players around."""
        table['HERE'] = ([0, 1, 2, 3, 4, 5, 6, 14, 7, 8, 9, 10, 11, 12, 13, 15, 16,
                          17, 18, 19, 20, 21, 22, 23, 24, 25, 26])[:len(table)]
        return table


if __name__ == '__main__':
    import yaml
    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        priv_d = yaml.load(_private)
        print(priv_d)

    p = Parse()
    p.table_from_file(priv_d)  # read table from source
    p.print_table(p.team)
