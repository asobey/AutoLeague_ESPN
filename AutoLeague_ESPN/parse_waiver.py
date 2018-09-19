import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import os
import requests


class Parse(object):

    def __init__(self):
        self.POSITIONS = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']
        self.team = pd.DataFrame
        self.waiver = pd.DataFrame

    def create_waiver(self, private_data, position='none'):
        """Listing of "position" playerIds on the waiver. Excludes players not playing this week (BYE or real life FA)"""
        cookies = {
            'espn_s2': private_data['espn_s2'],
            'SWID': private_data['SWID']
        }

        # slot codes used to get the right page
        # slots = {'QB': 0, 'RB': 2, 'RB/WR': 3, 'WR': 4, 'TE': 6, 'D/ST': 16, 'K': 17, 'FLEX': 23}

        if position == 'none':
            parameters = {'leagueId': private_data['leagueid'], 'teamID': private_data['teamid'],
                          'avail': 1, 'injury': 2, 'context': 'freeagency', 'view': 'overview'}
        else:
            parameters = {'leagueId': private_data['leagueid'], 'teamID': private_data['teamid'],
                          'slotCategoryId': position, 'avail': 1, 'injury': 2, 'context': 'freeagency',
                          'view': 'overview'}

        df = pd.DataFrame(columns=['Projected', 'PlayerId'])

        for si in [0]:  # just use the first pages for now. not sure why the third isn't working with si 50 and 100
            parameters['startIndex'] = si
            r = requests.get('http://games.espn.com/ffl/freeagency',
                             params=parameters,
                             cookies=cookies)

            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table', class_='playerTableTable')
            tdf = pd.read_html(str(table), flavor='bs4')[0]  # returns a list of df's, grab first
            tdf = tdf.iloc[2:, [13]]  # delete the useless columns
            table_line = str(soup.find_all("td", {"class": "playertablePlayerName"}))
            tdf['ID'] = list(map(int, re.findall('playername_(\d+)', table_line)))
            tdf.columns = ['Projected', 'PlayerId']
            df = df.append(tdf, ignore_index=True,
                           sort=False)  # !!!! non-concatenation axis is not aligned. remove the "sort=false" to troubleshoot

        df.query('Projected != "--"', inplace=True)  # Delete the players with "--"
        df['Projected'] = df['Projected'].fillna(0).astype('float')  #
        self.waiver = df
        return df

    def print_waiver(self):
        """Simply prints table in nice format"""
        print(tabulate(self.waiver, headers='keys', tablefmt='psql'))


if __name__ == '__main__':
    import yaml
    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        priv_d = yaml.load(_private)
        # print(priv_d)

    p = Parse()
    p.create_waiver(priv_d, 'QB')  # read waiver from web
    p.print_waiver()
