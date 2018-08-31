import requests
from lxml import html
from selenium import webdriver
working = 'online'

def retrieve_homepage(on_off):
    if on_off == 'online': # if online the use browser
        browser = webdriver.Firefox()
        #browser.get('http://games.espn.com/ffl/clubhouse?leagueId=413011&teamId=1&seasonId=2015#')
        browser.get('http://games.espn.com/ffl/clubhouse?leagueId=413011&teamId=1&seasonId=2018')
        if browser.title != 'The Big D- Sobauchery - ESPN':
            print('You are on the wrong page!')
        else:
            print('FF Page Opened.')
        # always save source file of homepage. This file can be used later for offine use or other module without
        # going online again
        _page_source = open('..\\offline_webpages\\front_page_source', 'w')
        _page_source.write(browser.page_source)
        _page_source.close()

    _browser2 = open('..\\offline_webpages\\front_page_source', 'r')
    return _browser2

if __name__ == '__main__':
    page_source = retrieve_homepage(working)

    for player_starting in range(3,12):
        print(page_source.find_element_by_xpath(
            '/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr['
                + str(player_starting) + ']/td[1]').text, end=' ')
        print(page_source.find_element_by_xpath(
            '/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr['
            + str(player_starting) + ']/td[2]').text)
        print(page_source.find_element_by_xpath(
            '/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr['
            + str(player_starting) + ']/td[9]').text)

    for bench_spot in range(15,18):
        print(page_source.find_element_by_xpath(
            '/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr['
                + str(bench_spot) + ']/td[1]').text, end=' ')
        print(page_source.find_element_by_xpath(
            '/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr['
            + str(bench_spot) + ']/td[2]').text)
        print(page_source.find_element_by_xpath(
            '/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr['
            + str(bench_spot) + ']/td[9]').text)
