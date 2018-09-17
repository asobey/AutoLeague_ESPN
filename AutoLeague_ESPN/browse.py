from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
# program imports
from AutoLeague_ESPN.manage import import_yaml


class Browse(object):
    """Creates a Selenium webdriver object"""

    def __init__(self):
        self.private_data = import_yaml()
        self.homepage = self.private_data['homepage']
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

    #This probably needs to move to the logic module
    @staticmethod
    def handle_multi_spot_move(self, team_table, opt_team_chart):
        """The ESPN website does not allow for player in RB1 slot to move to RB1 and vice-versa. This is also true for WR1
        and WR2. This function can only handle leagues with 2 RBs and/or 2 WR2. Two QB or any other multi spot positions
        with throw an exception at the end."""
        for key, value in opt_team_chart.items():
            if key == 1 and team_table['HERE'].loc[team_table['ID'] == value].item() == 2:
                _temp1 = opt_team_chart[1]
                opt_team_chart[1] = opt_team_chart[2]
                opt_team_chart[2] = _temp1
            elif key == 3 and team_table['HERE'].loc[team_table['ID'] == value].item() == 4:
                _temp1 = opt_team_chart[3]
                opt_team_chart[3] = opt_team_chart[4]
                opt_team_chart[4] = _temp1
        return opt_team_chart

    def sort_team(self, team_table, opt_team_chart):
        """This funtion goes through the optimal team chart and calls the move function for each player change"""
        opt_team_chart = self.handle_multi_spot_move(team_table, opt_team_chart)

        for key, value in opt_team_chart.items():
            time.sleep(.5)  # UNNEEDED BUT LOOKS COOL
            if team_table['ID'].loc[team_table['HERE'] == key].item() == value:
                print(f'Spot: {key} already filled with player: {value}')
            else:
                print(
                    f'+++++++++++++++++++++++++++++++++++++++++++++Player: {value} needs to be moved to: {key}++++++++')
                try:
                    self.id_to_here(value, key)
                except NotImplementedError:(f'Unable to move {value}')

if __name__ == '__main__':

    print('CWD: ', os.getcwd())  # can get rid of later. Should not hurt
    d = Browse()

    #browser_functions.save_source(browser, source_file_location, source_file_name)  # Save Source
    #team_table = team_table_parse.create_team_table(source_file_location, source_file_name)
    #team_table_parse.print_table(team_table)
