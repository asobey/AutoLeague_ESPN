# Intended for debugging in console
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import yaml
import os
import time

# BRING IN YAML
private = open(os.path.join('\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r')
privateData = yaml.load(private)

# GO TO HOMEPAGE
browser = webdriver.Firefox()
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
time.sleep(2)
actions = ActionChains(browser)
# For some reason extra Key.TAB is required at beginning on 2nd computer. Code not robust.
actions.send_keys(privateData['user'], Keys.TAB, privateData['pass'], Keys.ENTER)
actions.perform()

