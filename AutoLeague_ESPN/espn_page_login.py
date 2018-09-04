from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import yaml
import os


def login_and_return_browser():
    privateData = import_yaml()
    browser = open_browser(privateData)
    # RESIZE WINDOW
    browser.set_window_size(1100, 1080)
    browser = navigate_and_login(browser, privateData)
    return browser


def import_yaml():
    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        try:
            privateData = yaml.load(_private)
            return privateData
        except yaml.YAMLError as exc:
            print(exc)


def open_browser(privateData):
    browser = webdriver.Chrome() # For some reason the webdriver.Chrome() window does not come up big enough to
    # find the proper login button. Firefox opens a large enough window. It is failing to login possible resizing or
    # other method may be required.
    try:
        browser.get(privateData['homepage'])
        print('Fantasy Football Page Opened.')
        return browser
    except:
        print('Error Opening Homepage')
    return browser


def navigate_and_login(browser, _privateData):
    time.sleep(.1)
    # set window size
    browser.set_window_size(1100, 1080)


def navigate_and_login(browser, _privateData):
    # select corner profile
    ProfileElem = browser.find_element_by_link_text('Log In')
    ProfileElem.click()
    time.sleep(.5)
    # select login
    LoginElem = browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td/div[2]/div[2]/header/div[2]/ul/li[2]/div/div/ul[1]/li[4]/a')
    LoginElem.click()
    time.sleep(.5)
    # fill username and password with keystokes
    time.sleep(2)
    actions = ActionChains(browser)
    # For some reason extra Key.TAB is required at beginning on 2nd computer. Code not robust.
    actions.send_keys(_privateData['user'], Keys.TAB, _privateData['pass'], Keys.ENTER)
    actions.perform()
    return browser


if __name__ == '__main__':

    import AutoLeague_ESPN.browser_functions as browser_functions
    import AutoLeague_ESPN.team_table_parse as team_table_parse

    source_file_location = '..\\offline_webpages\\'
    source_file_name = 'front_page_source'

    browser = login_and_return_browser()

    browser_functions.save_source(browser, source_file_location, source_file_name)  # Save Source

    time.sleep(3)
    team_table = team_table_parse.update_team_table(browser.page_source)  # read table from source
    team_table_parse.print_table(team_table)
