import AutoLeague_ESPN as espn_page_login
import AutoLeague_ESPN as team_table_parse
import AutoLeague_ESPN as browser_functions

import os.path

# option to work online/offline is included for troublshooting quickly (not openning the same browser window repeatedly
work = 'online' # 'offline' or 'online'
source_file_location = '..\\offline_webpages\\'
source_file_name = 'front_page_source'


if __name__ == '__main__':
    # +++ONLINE+++
    if work == 'online':
        browser = espn_page_login.login_and_return_browser() #Login

        browser_functions.save_source(browser, source_file_location, source_file_name) # Save Source

        team_table = team_table_parse.create_team_table(source_file_location, source_file_name) # Make Team Table
        team_table_parse.print_table(team_table) # Print Table


    # +++OFFLINE+++
    elif work == 'offline':
        if os.path.isfile(source_file_location + source_file_name):
            team_table = team_table_parse.create_team_table(source_file_location, source_file_name)
            team_table_parse.print_table(team_table)
        else:
            raise NameError('Offline file does not exist')



    # +++ERROR+++
    else:
        raise NameError('[work] argument not properly defined')

