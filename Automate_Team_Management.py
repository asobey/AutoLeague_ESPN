# Automate_Team_Management is the main file used to handle ESPN Fantasy Football (FF)
# Team Management. This is meant to handle an entire season without users input.
# GOALS:
# 1) Set weekly line-ups (put high scorers in, take low scorers/non players out)
# 2) Frequent the waiver wire and pickup better players
# 3) Offer trades (offset to owners team)
#
# One required file that I do not have on GitHub is the username/password keeper.
# Please create this file and place it in the same directory to use this program.
# It consists of only two lines (below) and requires your ESPN username and password.
# Filename: espn_creds.yaml
# ESPNUserName: xxxxxxxxxx@xxxxxxxxx.com
# routerPassword: xxxxxxxxxxxx

import requests, time, yaml
from bs4 import BeautifulSoup
from selenium import webdriver

work = 'offline' # 'offline' or 'online'

def open_and_login():
    browser = webdriver.Firefox()
    browser.get('http://games.espn.com/ffl/clubhouse?leagueId=413011&teamId=1&seasonId=2015#')
    if browser.title != 'The Big D- Sobauchery - ESPN':
        print('You are on the wrong page!')
    else:
        print('FF Page Opened.')
    return browser.page_source #r eturn page source

def read_front_table(page_source):
    print('Read Front Table Started...')
    soup = BeautifulSoup(page_source, 'html.parser') # start parse with BS
    #print(soup.prettify())

    #soup.find('td', text = 'QB')
    print(soup.find("tr", id="plyr12483"))
    soup.find("tr", {"class": "pncPlayerRow playerTableBgRow0"})
    soup.find("tr", {"class": "pncPlayerRow"}).text
    for player in range(12):
        print(soup.find("tr", {"class": f"pncPlayerRow playerTableBgRow{player}"}).text)


def scrape_front_page():
    results = requests.get("http://games.espn.com/ffl/clubhouse?leagueId=413011&teamId=1&seasonId=2015#")

    if results.status_code != 200:
        print('results.status_code error. Alert owner!')

    c = results.content
    #print(c)
    #soup


if __name__ == '__main__':
    if work == 'online':
        with open('espn_creds.yaml', 'r') as private:
            try:
                privateData = yaml.load(private)
            except yaml.YAMLError as exc:
                print(exc)

        page_source = open_and_login()
        PS = open('front_page_source', 'w')
        PS.write(page_source)
        PS.close()
    PS = open('front_page_source', 'r')
    read_front_table(PS)



