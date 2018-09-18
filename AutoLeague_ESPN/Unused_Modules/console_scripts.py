import time
import os

os.getcwd()
os.chdir('C:\\Users\\alexs\\PycharmProjects\\AutoLeague_ESPN\\AutoLeague_ESPN')

source_file_location = '..\\offline_webpages\\'
source_file_name = 'front_page_source'

import AutoLeague_ESPN as espn_page_login
import AutoLeague_ESPN as pandas_bs4_table_parse

browser = espn_page_login.login_and_return_browser()

team_table = pandas_bs4_table_parse.create_team_table(source_file_location, source_file_name)

print(team_table)

time.sleep(5)
move1 = browser.find_element_by_css_selector('#pncButtonMove_' + str(team_table['ID'][2]))
move1.click()

here2 = browser.find_element_by_css_selector('#pncButtonHere_' + str(team_table['HERE'][12]))

submit = browser.find_element_by_css_selector('#pncSaveRoster1')




here2.click()
submit.click()