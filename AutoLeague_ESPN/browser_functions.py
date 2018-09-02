"""
All browser controls located in this file
"""

"""
This module controls in browser movement. Several function accomplish movement in diffent ways.
"""

def save_source(browser, source_file_location, source_file_name):
    _PS = open((source_file_location + source_file_name), 'w')
    _PS.write(browser.page_source)
    _PS.close()


def id_to_here(browser, from_id, here_slot):
    """"move by player ID to HERE slot"""
    print(f'moving..... ID: {from_id} to HERE slot: {here_slot}')
    move1 = browser.find_element_by_css_selector('#pncButtonMove_' + str(from_id))
    move1.click()
    here2 = browser.find_element_by_css_selector('#pncButtonHere_' + str(here_slot))
    submit = browser.find_element_by_css_selector('#pncSaveRoster1')

    here2.click()
    submit.click()
    return browser


if __name__ == '__main__':
    import time
    import os

    import AutoLeague_ESPN.espn_page_login as espn_page_login
    import AutoLeague_ESPN.team_table_parse as team_table_parse

    print('CWD: ', os.getcwd()) #  can get rid of later. Should not hurt
    os.chdir('C:\\Users\\alexs\\PycharmProjects\\AutoLeague_ESPN\\AutoLeague_ESPN')

    print('CWD: ', os.getcwd()) #  can get rid of later. Should not hurt
    os.chdir('C:\\Users\\alexs\\PycharmProjects\\AutoLeague_ESPN\\AutoLeague_ESPN')

    source_file_location = '..\\offline_webpages\\'
    source_file_name = 'front_page_source'

    browser = espn_page_login.login_and_return_browser() # open browser and login

    save_source(browser, source_file_location, source_file_name) # save source
    team_table = team_table_parse.create_team_table(source_file_location, source_file_name) # read table from source

    team_table_parse.print_table(team_table)

    time.sleep(5)
    #Options to query on column to another: df[df['B']==3]['A'].item() ; df.query('B==3')['A'].item()
    from_ID = team_table[team_table['PLAYER']=='Joe Mixon, Cin RB']['ID'].item()
    to_HERE = team_table[team_table['PLAYER']=='Ronald Jones, TB RB']['HERE'].item()

    print('Switch ', team_table[team_table['ID']==from_ID]['PLAYER'].item(), ' and ', team_table[team_table['HERE']==to_HERE]['PLAYER'].item())
    browser = (browser, from_ID, to_HERE)

    time.sleep(5)
    source_file_name = 'temp1'
    # It takes these two steps to update table...possible improvement
    save_source(browser, source_file_location, source_file_name) # save source
    team_table = team_table_parse.create_team_table(source_file_location, source_file_name) # read table from source

    team_table_parse.print_table(team_table)
