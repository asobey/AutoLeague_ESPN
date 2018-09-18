import os
"""
All browser controls located in this file
"""

"""
This module controls in browser movement. Several function accomplish movement in diffent ways.
"""


def save_source(webdriver, source_file_location, source_file_name):
    source_path = os.path.join(source_file_location, source_file_name)
    print('Saving source_page to: ' + source_path, end='')
    _PS = open(source_path, 'w', encoding="utf-8")
    _PS.write(webdriver.page_source)
    _PS.close()
    print('.......DONE')


def id_to_here(webdriver, from_id, here_slot):
    """"move by player ID to HERE slot"""
    print(f'moving..... ID: {from_id} to HERE slot: {here_slot}')
    move1 = webdriver.find_element_by_css_selector('#pncButtonMove_' + str(from_id))
    move1.click()
    try:
        here2 = webdriver.find_element_by_css_selector('#pncButtonHere_' + str(here_slot))
        submit = webdriver.find_element_by_css_selector('#pncSaveRoster1')
        time.sleep(.2)
        here2.click()
        time.sleep(.2)
        submit.click()
    except:
        print('Multi spot anomaly detected!')

#THIS SHOULD AND IS HANDLED IN OPTIMIZE_TEAM
# def handle_multi_spot_move(team_table, opt_team_chart):
#     '''The ESPN website does not allow for player in RB1 slot to move to RB1 and vice-versa. This is also true for WR1
#     and WR2. This function can only handle leagues with 2 RBs and/or 2 WR2. Two QB or any other multi spot positions
#     with throw an exception at the end.'''
#     for key, value in opt_team_chart.items():
#         if key == 1 and team_table['HERE'].loc[team_table['ID'] == value].item() == 2:
#             _temp1 = opt_team_chart[1]
#             opt_team_chart[1] = opt_team_chart[2]
#             opt_team_chart[2] = _temp1
#         elif key == 3 and team_table['HERE'].loc[team_table['ID'] == value].item() == 4:
#             _temp1 = opt_team_chart[3]
#             opt_team_chart[3] = opt_team_chart[4]
#             opt_team_chart[4] = _temp1
#     return opt_team_chart

def sort_team(team_table, opt_team_chart):
    """This funtion goes through the optimal team chart and calls the move function for each player change"""
    #opt_team_chart = handle_multi_spot_move(team_table, opt_team_chart)

    for key, value in opt_team_chart.items():
        time.sleep(.5)  # UNNEEDED BUT LOOKS COOL
        if team_table['ID'].loc[team_table['HERE'] == key].item() == value:
            print(f'Spot: {key} already filled with player: {value}')
        else:
            print(f'+++++++++++++++++++++++++++++++++++++++++++++++Player: {value} needs to be moved to: {key}++++++++')
            try:
                id_to_here(browser, value, key)
            except:
                print(f'Unable to move {value}')


if __name__ == '__main__':
    import time

    import AutoLeague_ESPN.espn_page_login as espn_page_login
    import AutoLeague_ESPN.team_table_parse as team_table_parse
    import AutoLeague_ESPN.optimize_team as optimize_team

    print('CWD: ', os.getcwd()) #  can get rid of later. Should not hurt

    source_file_location = '..\\offline_webpages\\'
    source_file_name = 'front_page_source'
    source_path = os.path.join(source_file_location, source_file_name)

    browser = espn_page_login.login_and_return_browser()  # open browser and login

    time.sleep(3)

    save_source(browser, source_file_location, source_file_name) # save source
    team_table = team_table_parse.create_team_table(source_file_location, source_file_name) # read table from source
    team_table_parse.print_table(team_table)

    optimal_team_chart = optimize_team.optimize(team_table)
    optimal_team_table = optimize_team.optimize_position_table(team_table, optimal_team_chart)
    print('++++++++++++++++++OPTIMAL TEAM TABLE+++++++++++++++++++++')
    team_table_parse.print_table(optimal_team_table)

    sort_team(team_table, optimal_team_chart)