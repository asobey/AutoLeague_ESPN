from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate

working = 'online'
position = 'TE' # OPTIONS: QB, RB, RB/WR, WR, TE, FLEX, D/ST, K

if working == 'online': # setting up offline option so troublshooting can be done without
    # navigating to the website each time.
    browser = webdriver.Firefox()
    browser.get('http://games.espn.com/ffl/standings?leagueId=413011&seasonId=2018')

    standings_source = open('standings_page', 'w')
    standings_source.write(browser.page_source)
    standings_source.close()

PS = open('standings_page', 'r')
soup = BeautifulSoup(PS,'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))

#print(df)
print(tabulate(df[3], headers='keys', tablefmt='psql')) #table 3 appears to be the magic number