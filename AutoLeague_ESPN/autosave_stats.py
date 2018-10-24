# This file will save off stats, so they can be used later to refine the ranking algorithms

import yaml
import os
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


def import_yaml():
    """This function opens the espn_creds.yaml file and returns its contents as privateData"""
    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        try:
            private_data = yaml.load(_private)
            return private_data
        except yaml.YAMLError as exc:
            print(exc)


def get_waiver_source(pages=3, avail_request='available'):
    """Function to save all the waiver pages"""
    private_data = import_yaml()
    cookies = {'espn_s2': private_data['espn_s2'], 'SWID': private_data['SWID']}
    waiver_source_dict = {}
    availability_lookup = {'available': 1, 'full': -1}
    availability = availability_lookup[avail_request]  # adds the option to have a full player list, not just available players
    parameters = {'leagueId': private_data['leagueid'], 'teamID': private_data['teamid'],
                  'avail': availability, 'injury': 2, 'context': 'freeagency', 'view': 'overview'}
    print('Scraping waiver page:', end=' ', flush=True)
    for ix, start_index in enumerate(range(0, pages*50, 50)):  # Looks like start_index=1000 is the most ever used
        # Need to find some way to stop this from completing all the loops, if it gets to the end
        print(ix+1, '...', end=' ', flush=True)
        parameters['startIndex'] = start_index
        waiver_source_dict[ix] = requests.get('http://games.espn.com/ffl/freeagency', params=parameters,
                                              cookies=cookies)  # Fix multipage issue
    print()
    print('Note: only', len(waiver_source_dict), 'pages of the waiver were parsed. Modify browse.py if you want '
                                                 'greater depth')
    return waiver_source_dict


def waiver_table_from_source(waiver_source_dict):
    """Listing of "position" playerIds on the waiver. Excludes players not playing this week (BYE or real life
    FA)"""
    starttime = datetime.datetime.now()

    POSITIONS = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']
    df = pd.DataFrame()
    print('Parsing waiver page: ', end=' ', flush=True)
    for start_index in range(0, len(waiver_source_dict)):  #
        try:  # fix this as it loses out on the last page i think
            print(start_index+1, '...', end=' ', flush=True)
            soup = BeautifulSoup(waiver_source_dict[start_index].content, 'html.parser')
            table = soup.find('table', class_='playerTableTable')
            tdf = pd.read_html(str(table), flavor='bs4')[0]  # returns a list of df's, grab first
            print(datetime.datetime.now() - starttime)
            starttime = datetime.datetime.now()
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
            print(datetime.datetime.now() - starttime)
            starttime = datetime.datetime.now()
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
    df = add_position_col(df, POSITIONS)
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
    print(datetime.datetime.now() - starttime)
    return df[col_order]  # there is a better way to do this
#     C:\Python\Anaconda3\lib\site-packages\pandas\core\indexing.py:189: SettingWithCopyWarning:
# A value is trying to be set on a copy of a slice from a DataFrame


def add_position_col(table, positions):
    """This function finds the position of each player by parsing the 'PLAYER' column, then adds a 'POS' column with
    that value."""
    for pos in positions:
        pos_true = table.index[table['PLAYER'].str.contains('\xa0' + pos, na=False)].values
        table.loc[pos_true, 'POS'] = pos  # This is how to correctly set value in df
    return table


if __name__ == '__main__':

    full_waiver = waiver_table_from_source(get_waiver_source(20, 'full'))

    path = '..\\AutoLeague_ESPN'
    full_waiver.to_csv(os.path.join(path, datetime.date.today().isoformat() + '_waiver.csv'))  # Save to cvs and pickle
    print('Data for', len(full_waiver), 'players was stored to the CSV file in', path)
