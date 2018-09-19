import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import os
import requests


class Parse(object):

    def __init__(self):
        self.WAIVER_POS = ['QB', 'RB', 'RB/WR', 'WR', 'TE', 'FLEX', 'K', 'D/ST', 'ALL']
        self.waiver = {}

    def top_waiver(self, source_dict, position=None):
        """this "top" ranking is personal preference. initial setup is based on espn's projection"""
        if not position:
            self.waiver['ALL'] = self.create_waiver(source_dict).nlargest(20, 'PROJ')  # fix the [0] indicie
            print(tabulate(self.waiver['ALL'], headers='keys', tablefmt='psg1'))
        else:
            for pos in self.WAIVER_POS:
                self.waiver[pos] = self.create_waiver(source_dict[pos[0]], pos).nlargest(3, 'PROJ')  # fix the [0] indicie
                print(pos)
                print(tabulate(self.waiver[pos], headers='keys', tablefmt='psg1'))
        # maybe do a reindex or something?
        # print(tabulate(player, headers='keys', tablefmt='psg1'))

    def create_waiver(self, waiver_source_dict):
        """Listing of "position" playerIds on the waiver. Excludes players not playing this week (BYE or real life FA)"""

        df = pd.DataFrame()

        for start_index in range(0, len(waiver_source_dict)):  #
            try:  # fix this as it loses out on the last page i think
                soup = BeautifulSoup(waiver_source_dict[start_index].content, 'html.parser')
                table = soup.find('table', class_='playerTableTable')
                tdf = pd.read_html(str(table), flavor='bs4')[0]  # returns a list of df's, grab first
                tdf = tdf.iloc[2:, [0, 2, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 17]]  # Identify the columns you want to keep by deleting the useless columns
                # tdf = tdf.iloc[2:, [13]]  # delete the useless columns
                table_line = str(soup.find_all("td", {"class": "playertablePlayerName"}))
                tdf['ID'] = list(map(int, re.findall('playername_(\d+)', table_line)))
                # tdf.columns = ['Projected', 'PlayerId']  # fill these in fully
                df = df.append(tdf, ignore_index=True,
                               sort=False)  # !!!! non-concatenation axis is not aligned. remove the "sort=false" to troubleshoot
            except:
                pass
        df.columns = ['Player', 'Waiver Day', 'Team', 'Game Time', 'PRK', 'PTS', 'AVG', 'LAST', 'PROJ', 'OPRK', '%ST',
                      '%OWN', '+/-', 'ID']
        df.query('PROJ != "--"', inplace=True)  # Delete the players with "--"
        df['PROJ'] = df['PROJ'].fillna(0).astype('float')  #
        col_order = ['Player', 'Waiver Day', 'Team', 'Game Time', 'PRK', 'PTS', 'AVG', 'LAST', 'PROJ', 'OPRK', '%ST',
                      '%OWN', '+/-', 'ID'] # Changing col order for user UPDATE!!!!
        dfaa = df[col_order]  # there is a better way to do this
        # print(tabulate(dfaa, headers='keys', tablefmt='psg1'))

        return dfaa


if __name__ == '__main__':
    import yaml
    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        priv_d = yaml.load(_private)
        # print(priv_d)

    p = Parse()
    p.top_waiver(priv_d)  # read waiver from web

