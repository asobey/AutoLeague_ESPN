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
        # self.homepage = self.private_data['homepage']
        self.homepage = 'http://games.espn.com/ffl/clubhouse?leagueId={0}&teamId={1}&seasonId={2}'.format(
            self.private_data['leagueid'], self.private_data['teamid'], self.private_data['seasonid'])
        self.cookies = {'espn_s2': self.private_data['espn_s2'], 'SWID': self.private_data['SWID']}
        self.driver = object

    def get_team_page_source(self):
        r = requests.get(self.homepage,
                         cookies=self.cookies)
        return r.content

    def initialize_browser(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1100, 1080)  # width, length.
        self.driver.get(self.homepage)

        if self.private_data['login_by'] == 'cookies':
            self.login_by_cookies()
        elif self.private_data['login_by'] == 'cred':
            self.login_by_creds()
        else:
            raise NameError('login_by not properly specified')
        # Webdriver wait to make sure everything loads before object is complete
        WebDriverWait(self.driver, 8).until(lambda driver: self.driver.find_element_by_class_name('eplus'))

    def login_by_cookies(self):
        """This function adds cookies to the browser, thereby logging in"""
        cookies = {'espn_s2': self.private_data['espn_s2'], 'SWID': self.private_data['SWID']}
        for cookie in cookies:
            c = {'name': cookie, 'value': cookies[cookie]}  # Revisit for understanding cookies[n]?
            self.driver.add_cookie(c)
        self.driver.get(self.homepage)
        assert "Log In" not in self.driver.title  # Make sure the you are logged in by checking for 'Log In' not there

    def login_by_creds(self):
        """This function logs into the homepage after the browser is open by use of credentials."""
        corner_elem_text = 'Log In'
        login_button_xpath = '/html/body/div[2]/table/tbody/tr/td/div[2]/div[2]/header/div[2]/ul/li[2]/div/div/ul[1]/' \
                             'li[4]/a'
        # Click corner profile menu
        profile_elem = WebDriverWait(self.driver, 10).until(
            lambda: self.driver.find_element_by_link_text(corner_elem_text))
        profile_elem.click()
        # Select 'Login' from profile menu
        login_elem = WebDriverWait(self.driver, 10).until(lambda: self.driver.find_element_by_xpath(login_button_xpath))
        login_elem.click()
        # ****FIX DESIRED***: Wait for login popup. Currently cannot identify element to wait on.
        time.sleep(2)
        # Fill username and password with key-stokes
        actions = ActionChains(self.driver)
        # For some reason extra Key.TAB is required at beginning on 2nd computer (old laptop). Code not robust.
        actions.send_keys(self.private_data['user'], Keys.TAB, self.private_data['pass'], Keys.ENTER)
        actions.perform()

    def save_source(self):
        """Function to save page source from the webdriver"""
        source_path = os.path.join(self.private_data['source_file_location'], self.private_data['source_file_name'])
        print('Saving source_page to: ' + source_path, end='')
        with open(source_path, 'w', encoding="utf-8") as _PS:
            _PS.write(self.driver.page_source)
            print('.......DONE')

    def id_to_here(self, from_id, here_slot):
        """"move by player ID to HERE slot"""
        print(f'moving..... ID: {from_id} to HERE slot: {here_slot}')
        try:
            move1 = self.driver.find_element_by_css_selector('#pncButtonMove_' + str(from_id))
            move1.click()
            try:
                here2 = self.driver.find_element_by_css_selector('#pncButtonHere_' + str(here_slot))
                submit = self.driver.find_element_by_css_selector('#pncSaveRoster1')
                time.sleep(.2)
                here2.click()
                time.sleep(.2)
                submit.click()
            except NotImplementedError:
                print('Multi spot anomaly detected!')
            except:
                move1 = self.driver.find_element_by_css_selector('#pncButtonMoveSelected_' + str(from_id))
                move1.click()
                print(f"--> Unable to click on slot {here_slot}'s HERE button!")
        except:
            print(f"--> Unable to click on {from_id}'s move button!")

    def sort_team(self, team_table, opt_team_chart):
        """This function goes through the optimal team chart and calls the move function for each player change"""
        # opt_team_chart = self.handle_multi_spot_move(team_table, opt_team_chart)

        for key, value in opt_team_chart.items():
            time.sleep(.5)  # UNNEEDED BUT LOOKS COOL
            if team_table['ID'].loc[team_table['HERE'] == key].item() == value:
                print(f'Spot: {key} already filled with player: {value}')
            else:
                print(f'+++++++++++++++++++++++++++++++++++++++++ Player: {value} needs to be moved to: {key} ++++++++')
                try:
                    self.id_to_here(value, key)
                except NotImplementedError:
                    print(f'Unable to move {value}')

    def get_waiver_source(self, pages=3, avail_request='available'):
        """Function to save all the waiver pages"""
        cookies = {'espn_s2': self.private_data['espn_s2'], 'SWID': self.private_data['SWID']}
        waiver_source_dict = {}
        availability_lookup = {'available': 1, 'full': -1}
        availability = availability_lookup[avail_request]  # adds the option to have a full player list, not just available players
        parameters = {'leagueId': self.private_data['leagueid'], 'teamID': self.private_data['teamid'],
                      'avail': availability, 'injury': 2, 'context': 'freeagency', 'view': 'overview'}
        for ix, start_index in enumerate(range(0, pages*50, 50)):  # Looks like start_index=1000 is the most ever used
            # Need to find some way to stop this from completing all the loops, if it gets to the end
            print('Scraping waiver page:', ix+1, '...', end=' ', flush=True)
            parameters['startIndex'] = start_index
            waiver_source_dict[ix] = requests.get('http://games.espn.com/ffl/freeagency', params=parameters,
                                                  cookies=cookies)  # Fix multipage issue
        print()
        print('Note: only', len(waiver_source_dict), 'pages of the waiver were parsed. Modify browse.py if you want '
                                                     'greater depth')
        return waiver_source_dict


if __name__ == '__main__':
    print('CWD: ', os.getcwd())  # can get rid of later. Should not hurt
    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        priv_data = yaml.load(_private)
    browse = Browse(priv_data)
    print(browse.cookies)
    print(browse.get_waiver_source())
