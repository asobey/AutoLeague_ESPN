from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time
import yaml
import os


def login_and_return_browser():
    """This function calls the import_yaml function to open espn_cred.yaml file then calls the navigate_and_login
    function. It does not return anything but starts the webdriver/broswer object'"""
    private_data = import_yaml()
    webdriver = open_browser(private_data)
    # RESIZE WINDOW
    webdriver.set_window_size(1100, 1080)  # width, length. This is needed to be able to select profile menu
    webdriver = navigate_and_login(webdriver, private_data)
    return webdriver


def import_yaml():
    """This function opens the espn_creds.yaml file and returns its contents as privateData"""
    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        try:
            private_data = yaml.load(_private)
            return private_data
        except yaml.YAMLError as exc:
            print(exc)


def open_browser(private_data):
    """This function simply opens and returns the webdriver/browser"""
    browser = webdriver.Chrome()
    try:
        browser.get(private_data['homepage'])
        print('Fantasy Football Page Opened.')
        return browser
    except:
        print('Error Opening Homepage')
    return browser


def navigate_and_login(browser, private_data):
    """This function navigates and logs into the homepage after the browser is open and loaded to the homepage."""
    corner_elem_text = 'Log In'
    login_button_xpath = '/html/body/div[2]/table/tbody/tr/td/div[2]/div[2]/header/div[2]/ul/li[2]/div/div/ul[1]/' \
                         'li[4]/a'
    # username_field = "//input[@placeholder='Username or Email Address']"
    username_field = '#did-ui-view > div > section > section > form > section > div:nth-child(1) > div > label > span.input-wrapper > input'
    action_xpath = '//*[@id="playertable_0"]/tbody/tr[2]/td[3]'

    # Click corner profile menu
    profile_elem = WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_link_text(corner_elem_text))
    profile_elem.click()
    # Select 'Login' from profile menu
    login_elem = WebDriverWait(browser,10).until(lambda browser: browser.find_element_by_xpath(login_button_xpath))
    login_elem.click()
    # <<<<<================ISSUE TO FIX======================================
    # ****FIX DESIRED***: Wait for login popup. Currently cannot identify element to wait on.
    time.sleep(2)
    pop_up = '// *[ @ id = "did-ui-view"]'
    #username_elem = WebDriverWait(browser, 5).until(lambda browser: browser.find_elements_by_id("did-ui-view"))
    #username_elem = WebDriverWait(browser, 5).until(lambda browser: browser.find_elements_by_css_selector(username_field))
    # Fill username and password with key-stokes
    actions = ActionChains(browser)
    # For some reason extra Key.TAB is required at beginning on 2nd computer (old laptop). Code not robust.
    actions.send_keys(private_data['user'], Keys.TAB, private_data['pass'], Keys.ENTER)
    actions.perform()

    # =====================ISSUE TO FIX=================================>>>>>
    # This WebDriverWait statement is to ensure broswer is not retuned until table is fully loaded. 'eplus' is a new
    # table tab that appears after login. Without this wait statement a smaller table is saved and parsing breaks.
    action_column = WebDriverWait(browser, 8).until(lambda browser: browser.find_element_by_class_name("eplus"))

    return browser


if __name__ == '__main__':

    import AutoLeague_ESPN.Unused_Modules.browser_functions as browser_functions
    import AutoLeague_ESPN.Unused_Modules.team_table_parse as team_table_parse

    source_file_location = '..\\offline_webpages\\'
    source_file_name = 'front_page_source'

    browser = login_and_return_browser()

    browser_functions.save_source(browser, source_file_location, source_file_name)  # Save Source
    team_table = team_table_parse.create_team_table(source_file_location, source_file_name)
    #team_table_parse.print_table(team_table)
