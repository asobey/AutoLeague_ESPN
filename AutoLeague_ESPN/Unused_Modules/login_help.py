#https://stackoverflow.com/questions/33326459/logging-into-espn-using-selenium

# #https://www.reddit.com/r/learnpython/comments/2pv118/selenium_and_logging_into_espn/
#
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
#
# url = 'http://games.espn.go.com/ffl/freeagency?leagueId=1104640&seasonId=2014'
# driver = webdriver.Chrome()
# driver.get(url)
# elem = driver.find_element_by_id('personalizationLink')
# elem.click()
# time.sleep(5)
# driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
# elem3 = driver.find_element_by_id('username')
# elem3.send_keys('xxxxx')



import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("http://games.espn.go.com/ffl/signin")
#implement wait it is mandatory in this case
WebDriverWait(driver,1000).until(EC.presence_of_all_elements_located((By.XPATH,"(//iframe)")))
frms = driver.find_elements_by_xpath("(//iframe)")

#driver.switch_to.frame(frms[len(frms)-1])
driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
elem3 = driver.find_element_by_id('username')
elem3.send_keys('xxxxx')

time.sleep(2)
driver.find_element_by_xpath("(//input)[1]").send_keys("username")
driver.find_element_by_xpath("(//input)[2]").send_keys("pass")
driver.find_element_by_xpath("//button").click()
driver.switch_to.default_content()
time.sleep(4)
driver.close()
#
# #//*[@id="did-ui-view"]/div/section/section/form/section/div[1]/div/label/span[2]/input