from selenium import webdriver
import yaml

with open('espn_creds.yaml', 'r') as private:
    try:
        privateData = yaml.load(private)
    except yaml.YAMLError as exc:
        print(exc)

browser = webdriver.Firefox()

browser.get('http://games.espn.com/ffl/clubhouse?leagueId=413011&teamId=1&seasonId=2018')
if browser.title != 'The Big D- Sobauchery - ESPN':
    print('You are on the wrong page!')
else:
    print('FF Page Opened.')

# select corner profile
ProfileElem = browser.find_element_by_link_text('Log In')
ProfileElem.click()
# select login
LoginElem = browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td/div[2]/div[2]/header/div[2]/ul/li[2]/div/div/ul[1]/li[4]/a')
LoginElem.click()
# fill username
UserElem = browser.find_elements_by_xpath('/html/body/div[2]/div/div/section/section/form/section/div[1]/div/label/span[2]/input')
UserElem = browser.find_elements_by_partial_link_text()
UserElem.send_keys(privateData.user)
# fill password


"//span[text()='Search by Hotel or City Name']"
