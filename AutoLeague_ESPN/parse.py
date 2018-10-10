import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import os


class Parse(object):

    def __init__(self):
        self.POSITIONS = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']
        self.team = pd.DataFrame
        self.waiver = pd.DataFrame

    def team_table(self, page_source=None):
        if page_source is not None:
            print('Using table from file.')
            self.table_from_source(page_source)

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
        for index in team_table:
            if team_table[4][index] == '** BYE **':
                for col in list(range(7,17))[::-1]:
                    team_table.loc[index, col] = team_table.loc[index, col-1]
                team_table.loc[index, 5] = '** BYE **'
        team_table = team_table.drop([2, 6, 11], axis=1)  # drops the unused columns
        # MAKE 1ST ROW COLUMN HEADERS AND DROP 1ST ROW
        team_table.columns = team_table.iloc[1]  # make 2nd row the column headers
        team_table = team_table.fillna('--')  # Fill nan values with -- makes them able to index of of later
        team_table = team_table[team_table.PROJ != 'PROJ']  # Removes the second header row
        team_table = team_table[team_table.PLAYER != '--']  # removes any unused roster slots from the table
        team_table = team_table.reset_index(drop=True)  # reindex
        # Set -1 for empty values of PROJ, LAST, and AVG. Makes easier to work with
        team_table.PROJ.loc[team_table.PROJ == '--'] = -1
        team_table.LAST.loc[team_table.LAST == '--'] = -1
        team_table.AVG.loc[team_table.AVG == '--'] = -1
        numeric_cols = ['PRK', 'LAST', 'PTS', 'AVG', 'PROJ', '%ST', '%OWN', '+/-']
        team_table[numeric_cols] = team_table[numeric_cols].apply(pd.to_numeric, errors='coerce')
        # REMOVE TABS Â
        team_table = team_table.replace('Â', '', regex=True)
        # Add column methods 3X
        team_table = self.add_position_col(team_table, self.POSITIONS)
        team_table = self.add_player_id(team_table, _table_soup)
        team_table = self.add_here_col(team_table)

        team_table = team_table.fillna('--')  # Again, fill nan values with -- makes them able to index of of later
        col_order = ['HERE', 'SLOT', 'POS', 'ID', 'PLAYER', 'PTS', 'AVG', 'LAST', 'PROJ', '%ST', '%OWN',
                     '+/-', 'OPRK', 'OPP', 'PRK', 'STATUS ET']  # Changing col order for user
        self.team = team_table[col_order]
        return self.team

    @staticmethod
    def add_player_id(team_table, table_soup):
        """This function searches the BS4 soup for each players ID then adds it"""
        table_line = str(table_soup.find_all("td", {"class": "playertablePlayerName"}))
        player_ids = list(map(int, re.findall('playername_(\d+)', table_line)))
        player_ids_insert = ['--'] * len(team_table)  # Start by filling all rows with '--'
        team_table['ID'] = player_ids_insert
        for i in team_table.index:
            if team_table['POS'][i] != '--':
                if len(player_ids) > 0:
                    team_table.loc[i, 'ID'] = player_ids[0]
                    player_ids.pop(0)
        return team_table

    @staticmethod
    def add_position_col(table, positions):
        """This function finds the position of each player by parsing the 'PLAYER' column, then adds a 'POS' column with
        that value."""
        for pos in positions:
            pos_true = table.index[table['PLAYER'].str.contains('\xa0' + pos, na=False)].values
            table.loc[pos_true, 'POS'] = pos  # This is how to correctly set value in df
        return table

    @staticmethod
    def add_here_col(table):
        """This function simply adds a 'HERE' column. HERE is the slot position recognized by the weddriver when moving
        players around. Need to make the HERE column more flexible with team"""
        table['HERE'] = ([0, 1, 2, 3, 4, 5, 6, 14, 7, 8, 9, 10, 11, 12, 13, 15, 16,
                          17, 18, 19, 20, 21, 22, 23, 24, 25, 26])[:len(table)]
        return table

    def waiver_table_from_source(self, waiver_source_dict):
        """Listing of "position" playerIds on the waiver. Excludes players not playing this week (BYE or real life
        FA)"""
        df = pd.DataFrame()
        print('Parsing waiver page: ', end=' ', flush=True)
        for start_index in range(0, len(waiver_source_dict)):  #
            try:  # fix this as it loses out on the last page i think
                print(start_index+1, '...', end=' ', flush=True)
                soup = BeautifulSoup(waiver_source_dict[start_index].content, 'html.parser')
                table = soup.find('table', class_='playerTableTable')
                tdf = pd.read_html(str(table), flavor='bs4')[0]  # returns a list of df's, grab first
                for index in tdf:
                    if tdf[5][index] == '** BYE **':
                        for col in list(range(8, 18))[::-1]:
                            tdf.loc[index, col] = tdf.loc[index, col - 1]
                            tdf.loc[index, 6] = '** BYE **'
                tdf = tdf.iloc[2:, [0, 2, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16,
                                    17]]  # Identify the columns you want to keep by deleting the useless columns
                table_line = str(soup.find_all("td", {"class": "playertablePlayerName"}))
                tdf['ID'] = list(map(int, re.findall('playername_(\d+)', table_line)))  # add the player ID
                # print(tabulate(tdf, headers='keys', tablefmt='psg1'))
                df = df.append(tdf, ignore_index=True, sort=False)
                # !!!! non-concatenation axis is not aligned. remove the "sort=false" to troubleshoot
            except ValueError:
                print('Looks like your cookies are not working properly')
                raise
            except LookupError:  # need to fix this to clarify what the error is that I'm looking for
                print()
                print('You ran into the last page of something, but that is ok for now')
                break
        print()
        # print(tabulate(df, headers='keys', tablefmt='psg1'))
        df.columns = ['PLAYER', 'Waiver Day', 'OPP', 'STATUS ET', 'PRK', 'PTS', 'AVG', 'LAST', 'PROJ', 'OPRK', '%ST',
                      '%OWN', '+/-', 'ID']
        #df['POS'] = df['Player'].str.split(',').str[1]  # parse out the position, part 1
        # if df['POS'].str.split().str[2] it contains the injury status, i think (Q, O, etc.)
        #df['POS'] = df['POS'].str.split().str[1]  # parse out the position (might be a better way of doing this)
        df['POS'] = ''
        df = self.add_position_col(df, self.POSITIONS)
        # df['Player'] = df['Player'].str.split(',').str[0]  # keep just player name
        # df.query('PROJ != "--"', inplace=True)  # Delete the players with "--", as these are not playing this week
        df = df.fillna('--')
        df.PROJ.loc[df.PROJ == '--'] = -1
        df.LAST.loc[df.LAST == '--'] = -1
        df.AVG.loc[df.AVG == '--'] = -1
        numeric_cols = ['PRK', 'LAST', 'PTS', 'AVG', 'PROJ', '%ST', '%OWN', '+/-']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        #df['PROJ'] = df['PROJ'].fillna(0).astype('float')
        col_order = ['Waiver Day', 'POS', 'ID', 'PLAYER', 'PTS', 'AVG', 'LAST', 'PROJ',  '%ST', '%OWN', '+/-', 'OPRK',
                     'OPP', 'PRK', 'STATUS ET']  # Changing col order for user UPDATE!!!!
        return df[col_order]  # there is a better way to do this
        '''
        C:\Python\Anaconda3\lib\site-packages\pandas\core\indexing.py:189: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
  self._setitem_with_indexer(indexer, value)
        '''

    @staticmethod
    def print_table(table):
        """Simply prints table in nice format"""
        print(tabulate(table, headers='keys', tablefmt='psql'))


if __name__ == '__main__':
    import yaml
    from AutoLeague_ESPN.browse import Browse

    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        priv_d = yaml.load(_private)
        print(priv_d)

    browse = Browse(priv_d)
    parse = Parse()
    # Get Current Team
    team = parse.table_from_source(browse.get_team_page_source())
    parse.print_table(team)

    waiver = parse.waiver_table_from_source(browse.get_waiver_source())
    parse.print_table(waiver)