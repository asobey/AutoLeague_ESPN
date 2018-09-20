from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import yaml
import requests


class Browse(object):
    """Creates a Selenium webdriver object"""

    def __init__(self, private_data):
        self.private_data = private_data

    def get_waiver_source(self, position='none'):
        """Function to save all the waiver pages"""
        cookies = {
            'espn_s2': self.private_data['espn_s2'],
            'SWID': self.private_data['SWID']
        }

        # slot codes used to get the correct waiver page
        slot_id_lookup = {'QB': 0, 'RB': 2, 'RB/WR': 3, 'WR': 4, 'TE': 6, 'D/ST': 16, 'K': 17, 'FLEX': 23}
        r = {}

        if position == 'none':
            parameters = {'leagueId': self.private_data['leagueid'], 'teamID': self.private_data['teamid'],
                          'avail': 1, 'injury': 2, 'context': 'freeagency', 'view': 'overview'}
            for ix, si in enumerate(range(0, 1000, 50)):  # check that this includes the last page
                try:
                    parameters['startIndex'] = si
                    r[ix] = requests.get('http://games.espn.com/ffl/freeagency',  # fix the multi page issue
                                              params=parameters,
                                              cookies=cookies)
                except:
                    print('Broke on', si, '!!!!')
                    return r
        else:
            WAIVER_POS = ['QB', 'RB', 'RB/WR', 'WR', 'TE', 'FLEX', 'K', 'D/ST']
            for pos in WAIVER_POS:
                parameters = {'leagueId': self.private_data['leagueid'], 'teamID': self.private_data['teamid'],
                              'slotCategoryId': slot_id_lookup[pos], 'avail': 1, 'injury': 2, 'context': 'freeagency',
                              'view': 'overview'}
                for ix, si in enumerate([0, 50, 100, 150, 200]):  # check that this includes the last page
                    try:
                        parameters['startIndex'] = si
                        r[pos[ix]] = requests.get('http://games.espn.com/ffl/freeagency',  # fix the multi page issue
                                         params=parameters,
                                         cookies=cookies)
                    except:
                        print('Broke on', si, '!!!!')
                        pass
        return r


if __name__ == '__main__':
    print('CWD: ', os.getcwd())  # can get rid of later. Should not hurt
    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        priv_data = yaml.load(_private)
    b = Browse(priv_data)
