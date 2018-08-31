import espn_page_login, pandas_bs4_table_parse
import os.path

# option to work online/offline is included for troublshooting quickly (not openning the same browser window repeatedly
work = 'online' # 'offline' or 'online'
source_file_location = '..\\offline_webpages\\'
source_file_name = 'front_page_source'

def save_source(browser, source_file_location, source_file_name):
    _PS = open((source_file_location + source_file_name), 'w')
    _PS.write(browser.page_source)
    _PS.close()

if __name__ == '__main__':
    # +++ONLINE+++
    if work == 'online':
        browser = espn_page_login.login_and_return_browser()
        save_source(browser, source_file_location, source_file_name)

        team_table = pandas_bs4_table_parse.create_team_table(source_file_location, source_file_name)
        pandas_bs4_table_parse.print_table(team_table)


    # +++OFFLINE+++
    elif work == 'offline':
        if os.path.isfile(source_file_location + source_file_name):
            team_table = pandas_bs4_table_parse.create_team_table(source_file_location, source_file_name)
            pandas_bs4_table_parse.print_table(team_table)
        else:
            raise NameError('Offline file does not exist')



    # +++ERROR+++
    else:
        raise NameError('[work] argument not properly defined')

