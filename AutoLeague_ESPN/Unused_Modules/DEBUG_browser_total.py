# Intended for debugging in console
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import yaml
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import re

# BRING IN YAML
print(os.getcwd())
private = open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r')
privateData = yaml.load(private)

# GO TO HOMEPAGE
browser = webdriver.Chrome()
browser.get(privateData['homepage'])

# RESIZE WINDOW
browser.set_window_size(1100, 1080)

# PROFILE CORNER BUTTON
ProfileElem = browser.find_element_by_link_text('Log In')
ProfileElem.click()

# LOGIN BUTTON
time.sleep(.5)
LoginElem = browser.find_element_by_xpath(
    '/html/body/div[2]/table/tbody/tr/td/div[2]/div[2]/header/div[2]/ul/li[2]/div/div/ul[1]/li[4]/a')
LoginElem.click()

# FILL IN USERNAME AND PASSWORD WITH SINGLE CHAIN ACTION
time.sleep(.5)
actions = ActionChains(browser)
# For some reason extra Key.TAB is required at beginning on 2nd computer. Code not robust.
actions.send_keys(privateData['user'], Keys.TAB, privateData['pass'], Keys.ENTER)
actions.perform()

# WAIT FOR BROWSER TO LOAD
time.sleep(2)

# # SAVING PAGE_SOURCE
# source_file_location = '..\\offline_webpages\\'
# source_file_name = 'front_page_source'
# print('Saving source_page to: ' + os.path.join(source_file_location, source_file_name), end='')
# _PS = open(os.path.join(source_file_location, source_file_name), 'w', encoding="utf-8")
# _PS.write(browser.page_source)
# _PS.close()
# print('.......DONE')
#
# # OPEN PAGE_SOURCE
# _PS = open(source_file_location + source_file_name, 'r')

# Instead of saving and opening (commented out above), just going to send the page source to BF4
_PS = browser.page_source

# MAKING TABLE
_soup = BeautifulSoup(_PS, 'lxml')  # Using BS4 to parse
_table_soup = _soup.find_all('table')[0]  # Finding the table element in the soup
_df = pd.read_html(str(_table_soup))  # Making the soup table element into a pandas df
_team_table = _df[3]  # From troubleshooting the third table is the team table

#print(tabulate(_team_table, headers='keys', tablefmt='psql'))  # DEBUG

_team_table = _team_table.fillna('--')  # Fill nan values will -- makes them able to index of of later

if len(_team_table.columns) == 16:  # If not a large enough pause is given before table the browser.source the table
    # will not full load. If this occurs the ACTION column is missing. Check table[2][1] == 'ACTION' as well
    raise Exception('full table not loaded')

_team_table[3][1, 13] = 'POS'  # need to set this early so nan value does not become index
_team_table = _team_table.drop([2, 6, 11], axis=1).drop([0, 12], axis=0)

# fix a couple column header labels
_team_table[1][1] = 'PLAYER'

# MAKE 1ST ROW COLUMN HEADERS AND DROP 1ST ROW
_team_table.columns = _team_table.iloc[0]  # make 1st row the column headers
_team_table = _team_table.drop([1]).reset_index(drop=True)  # drop 1st row (now column headers) and reindex

for col in _team_table:
    _team_table[col][:9] = pd.to_numeric(_team_table[col][:9], errors='ignore')
    _team_table[col][11:] = pd.to_numeric(_team_table[col][11:], errors='ignore')

#print(tabulate(_team_table, headers='keys', tablefmt='psql'))

#_ADDING POSITIONS COL
POSITIONS = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']
for pos in POSITIONS:
    pos_true = _team_table.index[_team_table['PLAYER'].str.contains('\xa0' + pos)].values
    _team_table['POS'][pos_true] = pos


#_team_table = add_player_id(_team_table, _table_soup)
table_line = str(_table_soup.find_all("td", {"class": "playertablePlayerName"}))
player_ids = list(map(int, re.findall('playername_(\d+)', table_line)))

# The extra '--' at the end and the [:17] are to resolve having or not having an IR spot
player_ids_insert = (player_ids[:10] + ['ID'] + player_ids[10:] + ['--'] + ['--'] + ['--'])[:17]
_team_table['ID'] = player_ids_insert


#team_table_out = add_here_col(_team_table)
if len(_team_table.index) == 17:
    _team_table['HERE'] = ([0, 1, 2, 3, 4, 5, 6, 14, 7, 8, 'HERE', 9, 10, 11, 12, 13, 14])
elif len(_team_table.index) == 16:
    _team_table['HERE'] = ([0, 1, 2, 3, 4, 5, 6, 14, 7, 8, 'HERE', 9, 10, 11, 12, 13])  # not sure which "here" number for IR. maybe not 13
elif len(_team_table.index) == 15:
    _team_table['HERE'] = ([0, 1, 2, 3, 4, 5, 6, 14, 7, 8, 'HERE', 9, 10, 11, 12])
else:
    print('table row out of range')

print(tabulate(_team_table, headers='keys', tablefmt='psql'))

