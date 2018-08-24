import requests
from lxml import html
from selenium import webdriver
working = 'online'
if working == 'online':
    browser = webdriver.Firefox()
    browser.get('http://games.espn.com/ffl/clubhouse?leagueId=413011&teamId=1&seasonId=2015#')
    if browser.title != 'The Big D- Sobauchery - ESPN':
        print('You are on the wrong page!')
    else:
        print('FF Page Opened.')
    page_source = open('front_page_content', 'w')
    page_source.write(browser.page_source)
    page_source.close()

#browser2 = webdriver.Firefox()
#browser2.get('file://front_page_content')
browser2 = open('front_page_source', 'r')

for player_starting in range(3,12):
    print(browser2.find_element_by_xpath(
        '/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr['
            + str(player_starting) + ']/td[1]').text, end=' ')
    print(browser2.find_element_by_xpath(
        '/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr['
        + str(player_starting) + ']/td[2]').text)
    print(browser2.find_element_by_xpath(
        '/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr['
        + str(player_starting) + ']/td[9]').text)

for bench_spot in range(15,18):
    print(browser2.find_element_by_xpath(
        '/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr['
            + str(bench_spot) + ']/td[1]').text, end=' ')
    print(browser2.find_element_by_xpath(
        '/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr['
        + str(bench_spot) + ']/td[2]').text)
    print(browser2.find_element_by_xpath(
        '/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr['
        + str(bench_spot) + ']/td[9]').text)

    #print(tree.xpath('// *[ @ id = "pncPlayerRow_0"] / td[9]'))
    #//*[@id="slot_2580"]
    #//*[@id="playername_2580"]
    #/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr[3]/td[9]
    #/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr[5]/td[9]
    #/html/body/div[2]/table/tbody/tr/td/div[3]/div/div/div/div[4]/div/div/div[3]/div[3]/div/div[2]/table[2]/tbody/tr/td/table/tbody/tr[15]/td[9]