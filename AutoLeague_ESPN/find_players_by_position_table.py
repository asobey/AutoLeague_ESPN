from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate

working = 'online'
position = 'TE' # OPTIONS: QB, RB, RB/WR, WR, TE, FLEX, D/ST, K

if working == 'online':
    browser = webdriver.Firefox()
    browser.get('http://games.espn.com/ffl/freeagency?leagueId=413011&seasonId=2018')

    position_link = browser.find_element_by_link_text(position)
    position_link.click()

    players_source = open('players_page', 'w')
    players_source.write(browser.page_source)
    players_source.close()

PS = open('players_page', 'r')
soup = BeautifulSoup(PS,'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))

#print(df)
print(tabulate(df[3], headers='keys', tablefmt='psql')) #table 3 appears to be the magic number
