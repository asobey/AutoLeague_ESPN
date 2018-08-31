from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import yaml

def login_and_return_browser():
    privateData = import_yaml()
    browser = open_browser(privateData)
    browser = navigate_and_login(browser, privateData)
    return browser

def import_yaml():
    with open('espn_creds.yaml', 'r') as _private:
        try:
            privateData = yaml.load(_private)
            return privateData
        except yaml.YAMLError as exc:
            print(exc)

def open_browser(privateData):
    browser = webdriver.Firefox() #For some reason if I use webdriver.Chrome() the window does not come up big enough to
    # find the proper login button. Firefox opens a large enough window. It is failing to login possible resizing or
    # other method may be required.
    try:
        browser.get(privateData['homepage'])
        print('Fantasy Football Page Opened.')
        return browser
    except:
        print('Error Opening Homepage')

def navigate_and_login(_browser, _privateData):
    # select corner profile
    ProfileElem = _browser.find_element_by_link_text('Log In')
    ProfileElem.click()
    time.sleep(.5)
    # select login
    LoginElem = _browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td/div[2]/div[2]/header/div[2]/ul/li[2]/div/div/ul[1]/li[4]/a')
    LoginElem.click()
    time.sleep(.5)
    # fill username and password with keystokes
    time.sleep(1)
    actions = ActionChains(_browser)
    actions.send_keys(_privateData['user'], Keys.TAB, _privateData['pass'], Keys.ENTER)
    actions.perform()
    return _browser

if __name__ == '__main__':
    login_and_return_browser()

#UserElem = browser.find_elements_by_xpath('/html/body/div[2]/div/div/section/section/form/section/div[1]/div/label/span[2]/input')
#UserElem = browser.find_elements_by_id('input.ng-pristine.ng-invalid.ng-invalid-required.ng-valid-pattern.ng-touched')
#input.ng-pristine.ng-invalid.ng-invalid-required.ng-valid-pattern.ng-touched
#UserElem.send_keys(privateData.user)
# fill password
