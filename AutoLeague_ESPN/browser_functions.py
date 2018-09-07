"""
All browser controls located in this file
"""

"""
This module controls in browser movement. Several function accomplish movement in diffent ways.
"""

def save_source(webdriver, source_file_location, source_file_name):
    print('Saving source_page to: ' + os.path.join(source_file_location, source_file_name), end='')
    _PS = open(os.path.join(source_file_location, source_file_name), 'w', encoding="utf-8")
    _PS.write(webdriver.page_source)
    _PS.close()
    print('.......DONE')


def id_to_here(webdriver, from_id, here_slot):
    """"move by player ID to HERE slot"""
    print(f'moving..... ID: {from_id} to HERE slot: {here_slot}')
    move1 = webdriver.find_element_by_css_selector('#pncButtonMove_' + str(from_id))
    move1.click()
    here2 = webdriver.find_element_by_css_selector('#pncButtonHere_' + str(here_slot))
    submit = webdriver.find_element_by_css_selector('#pncSaveRoster1')
    time.sleep(.2)
    here2.click()
    time.sleep(.2)
    submit.click()


def sort_team(webdriver, team_table, opt_team_chart):
    for key, value in opt_team_chart.items():
        time.sleep(.5)
        if team_table['ID'].loc[team_table['HERE'] == key].item() == value:
            print(f'Spot: {key} already filled with player: {value}')
        else:
            print(f'+++++++++++++++++++++++++++++++++++++++++++++++Player: {value} needs to be moved to: {key}++++++++')
            try:
                id_to_here(webdriver, value, key)
            except:
                print(f'Unable to move {value}')


if __name__ == '__main__':
    import time
    import os

    import AutoLeague_ESPN.espn_page_login as espn_page_login
    import AutoLeague_ESPN.team_table_parse as team_table_parse
    import AutoLeague_ESPN.optimize_team as optimize_team

    print('CWD: ', os.getcwd()) #  can get rid of later. Should not hurt
    #os.chdir('C:\\Users\\alexs\\PycharmProjects\\AutoLeague_ESPN\\AutoLeague_ESPN')

    source_file_location = '..\\offline_webpages\\'
    source_file_name = 'front_page_source'

    browser = espn_page_login.login_and_return_browser()  # open browser and login

    time.sleep(2)

    save_source(browser, source_file_location, source_file_name) # save source
    team_table = team_table_parse.create_team_table(source_file_location, source_file_name) # read table from source

    team_table_parse.print_table(team_table)
    #
    # time.sleep(1)
    # # Options to query on column to another: df[df['B']==3]['A'].item() ; df.query('B==3')['A'].item()
    # #J's
    # #from_ID = team_table[team_table['PLAYER']=='A.J. Green, Cin WR']['ID'].item()
    # #to_HERE = team_table[team_table['PLAYER']=='Demaryius Thomas, Den WR']['HERE'].item()
    #
    # # S's
    # from_ID = team_table[team_table['PLAYER'] == 'Joe Mixon, Cin RB']['ID'].item()
    # to_HERE = team_table[team_table['PLAYER'] == 'Marshawn Lynch, Oak RB']['HERE'].item()
    # # add a check that you are moving to a valid spot
    #
    # print('Switch ', team_table[team_table['ID'] == from_ID]['PLAYER'].item(), ' and ', team_table[team_table['HERE'] ==
    #                                                                                           to_HERE]['PLAYER'].item())
    # browser = id_to_here(browser, from_ID, to_HERE)
    #
    # time.sleep(2)
    #
    # save_source(browser, source_file_location, source_file_name)  # save source
    # team_table = team_table_parse.create_team_table(source_file_location, source_file_name)  # read table from source
    # team_table_parse.print_table(team_table)
    #
    # print('Move using IDs')
    # # S's
    # from_ID = '16725'
    # print(team_table[team_table['ID'] == from_ID])
    # print(team_table[team_table['ID'] == '14402'])
    # to_HERE = team_table[team_table['ID'] == '14402']['HERE'].item()
    # # add a check that you are moving to a valid spot
    #
    # print('Switch ', team_table[team_table['ID'] == from_ID]['PLAYER'].item(), ' and ', team_table[team_table['HERE'] ==
    #                                                                                           to_HERE]['PLAYER'].item())
    # browser = id_to_here(browser, from_ID, to_HERE)

    time.sleep(2)

    save_source(browser, source_file_location, source_file_name)  # save source
    team_table = team_table_parse.create_team_table(source_file_location, source_file_name)  # read table from source
    team_table_parse.print_table(team_table)

    optimal_team_chart = optimize_team.optimize(team_table)
    optimal_team_table = optimize_team.optimize_position_table(team_table, optimal_team_chart)
    print('++++++++++++++++++OPTIMAL TEAM TABLE+++++++++++++++++++++')
    team_table_parse.print_table(optimal_team_table)

    sort_team(browser, team_table, optimal_team_chart)
