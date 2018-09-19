import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import os
import requests


class Parse(object):

    def __init__(self):
        self.POSITIONS = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']
        self.WAIVER_POS = ['QB', 'RB', 'RB/WR', 'WR', 'TE', 'FLEX', 'K', 'D/ST']
        self.team = pd.DataFrame
        self.waiver = {}

    def top_waiver(self, private_data):
        """this "top" ranking is personal preference. initial setup is based on espn's projection"""
        # return dict looks like {'QB': qb_df, 'RB': rb_df...
        for pos in self.WAIVER_POS:
            self.waiver[pos] = self.create_waiver(private_data, pos).nlargest(3, 'PROJ')
            print(pos)
            print(tabulate(self.waiver[pos], headers='keys', tablefmt='psg1'))
        # player = df.nlargest(3, 'Projected') # move over to logic
        # maybe do a reindex or something?
        # print(tabulate(player, headers='keys', tablefmt='psg1'))

    def create_waiver(self, private_data, position='none', waiver_source=0):
        """Listing of "position" playerIds on the waiver. Excludes players not playing this week (BYE or real life FA)"""
        cookies = {
            'espn_s2': private_data['espn_s2'],
            'SWID': private_data['SWID']
        }

        # slot codes used to get the right page
        slot_id_lookup = {'QB': 0, 'RB': 2, 'RB/WR': 3, 'WR': 4, 'TE': 6, 'D/ST': 16, 'K': 17, 'FLEX': 23}

        if position == 'none':
            parameters = {'leagueId': private_data['leagueid'], 'teamID': private_data['teamid'],
                          'avail': 1, 'injury': 2, 'context': 'freeagency', 'view': 'overview'}
        else:
            parameters = {'leagueId': private_data['leagueid'], 'teamID': private_data['teamid'],
                          'slotCategoryId': slot_id_lookup[position], 'avail': 1, 'injury': 2, 'context': 'freeagency',
                          'view': 'overview'}

        df = pd.DataFrame()

        for si in [0]:  # just use the first pages for now. not sure why the third isn't working with si 50 and 100
            parameters['startIndex'] = si
            r = requests.get('http://games.espn.com/ffl/freeagency',
                             params=parameters,
                             cookies=cookies)

            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table', class_='playerTableTable')
            tdf = pd.read_html(str(table), flavor='bs4')[0]  # returns a list of df's, grab first
            tdf = tdf.iloc[2:, [0, 2, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 17]]  # Identify the columns you want to keep by deleting the useless columns
            # tdf = tdf.iloc[2:, [13]]  # delete the useless columns
            table_line = str(soup.find_all("td", {"class": "playertablePlayerName"}))
            tdf['ID'] = list(map(int, re.findall('playername_(\d+)', table_line)))
            # tdf.columns = ['Projected', 'PlayerId']  # fill these in fully
            df = df.append(tdf, ignore_index=True,
                           sort=False)  # !!!! non-concatenation axis is not aligned. remove the "sort=false" to troubleshoot
        # print(tabulate(df, headers='keys', tablefmt='psql'))
        df.columns = ['Player', 'Waiver Day', 'Team', 'Game Time', 'PRK', 'PTS', 'AVG', 'LAST', 'PROJ', 'OPRK', '%ST',
                      '%OWN', '+/-', 'ID']
        df.query('PROJ != "--"', inplace=True)  # Delete the players with "--"
        df['PROJ'] = df['PROJ'].fillna(0).astype('float')  #
        col_order = ['Player', 'Waiver Day', 'Team', 'Game Time', 'PRK', 'PTS', 'AVG', 'LAST', 'PROJ', 'OPRK', '%ST',
                      '%OWN', '+/-', 'ID'] # Changing col order for user UPDATE!!!!
        dfaa = df[col_order]
        return dfaa

    def print_waiver(self):
        """Simply prints table in nice format"""
        print(tabulate(self.waiver, headers='keys', tablefmt='psql'))


if __name__ == '__main__':
    import yaml
    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        priv_d = yaml.load(_private)
        # print(priv_d)

    p = Parse()
    p.top_waiver(priv_d)  # read waiver from web
    # p.print_waiver()
