# ---------------------------------------------------------
# Main file for Josh's architecture
# Every day: rob_waiver_wire()  # may be able to use AWS
#

# Pseudo code

import requests
from bs4 import BeautifulSoup
import pandas as pd
import yaml
import re
from tabulate import tabulate


with open('espn_creds.yaml', 'r') as _private:
    privateData = yaml.load(_private)    # pulls in the person specific data (teamId, cookies, etc)


def add_player_id(team_table, table_soup):  # Only works on table_soups that are fully populated with ONLY players
    """ Adds the player ID from the soup when it isn't readily available. """

    table_line = str(table_soup.find_all("td", {"class": "playertablePlayerName"}))
    team_table['ID'] = list(map(int, re.findall('playername_(\d+)', table_line)))
    return team_table


def create_roster():

    cookies = {
        'espn_s2': privateData['espn_s2'],
        'SWID': privateData['SWID']
    }

    parameters = {
        'leagueId': privateData['leagueid'], 'teamId': privateData['teamid'], 'seasonId': privateData['seasonid']
    }

    r = requests.get("http://games.espn.com/ffl/api/v2/rosterInfo",
                     params=parameters,
                     cookies=cookies)
    roster = r.json()
    rdf = []  # initialize the list so we can use append right away
    temp2 = roster['leagueRosters']['teams'][0]['slots']  # create a nested lists? of all the "slots". Includes empties.
    slots = ['QB', 'RB1', 'RB2', 'RB/WR', 'WR1', 'WR2', 'TE', 'FLEX',  # Individual row titles in the standard table
             'D/ST', 'K', 'Bench1', 'Bench2', 'Bench3', 'Bench4', 'Bench5', 'IR']
    pos_ids = {0: 'QB', 2: 'RB', 3: 'RB/WR', 4: 'WR', 6: 'TE', 23: 'FLEX', 17: 'K', 16: 'D/ST', 20: 'Bench', 21: 'IR'}
    i = 0
    for match in temp2:  # runs though the entries and appends
        if len(match) > 3:  # Check for blank slot
            rdf.append([match['slotCategoryId'],
                        match['player']['playerId']])
        else:
            rdf.append([slots[i], '--', '--', '--', '--', '--'])
        i = i+1

    # table_str = tabulate(rdf, headers='keys', tablefmt='psql')
    return rdf


def add_projected_values(player_list):
    print('Still need to add the projected values')
    return player_list


def create_waiver(position='none'):
    """Listing of "position" playerIds on the waiver. Excludes players not playing this week (BYE or real life FA)"""
    cookies = {
        'espn_s2': privateData['espn_s2'],
        'SWID': privateData['SWID']
    }

    # slot codes used to get the right page
    slots = {'QB': 0, 'RB': 2, 'RB/WR': 3, 'WR': 4, 'TE': 6, 'D/ST': 16, 'K': 17, 'FLEX': 23}

    if position == 'none':
        parameters = {'leagueId': privateData['leagueid'], 'teamID': privateData['teamid'],
                      'avail': 1, 'injury': 2, 'context': 'freeagency', 'view': 'overview'}
    else:
        parameters = {'leagueId': privateData['leagueid'], 'teamID': privateData['teamid'],
                      'slotCategoryId': position, 'avail': 1, 'injury': 2, 'context': 'freeagency',
                      'view': 'overview'}

    df = pd.DataFrame(columns=['Projected', 'PlayerId'])

    for si in [0]:  # just use the first pages for now. not sure why the third isn't working with si 50 and 100
        parameters['startIndex'] = si
        r = requests.get('http://games.espn.com/ffl/freeagency',
                         params=parameters,
                         cookies=cookies)

        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', class_='playerTableTable')
        tdf = pd.read_html(str(table), flavor='bs4')[0]  # returns a list of df's, grab first
        tdf = tdf.iloc[2:, [13]]  # delete the useless columns
        tdf = add_player_id(tdf, soup)
        tdf.columns = ['Projected', 'PlayerId']
        df = df.append(tdf, ignore_index=True, sort=False)  # !!!! non-concatenation axis is not aligned. remove the "sort=false" to troubleshoot

    df.query('Projected != "--"', inplace=True)  # Delete the players with "--"
    df['Projected'] = df['Projected'].fillna(0).astype('float')  #

    return df


def top_waiver(position='none'):
    """this "top" ranking is personal preference. initial setup is based on espn's projection"""

    df = create_waiver(position)
    player = df.nlargest(3, 'Projected')
    # maybe do a reindex or something?
    # print(tabulate(player, headers='keys', tablefmt='psg1'))

    return player


def sort_on_projected(roster):
    print('Still need to sort on projected')
    return roster


def rearrange_current_roster():  # eventually add something that fixes for Thursdays
    working_roster = create_roster()  # Builds the working file for the roster. Required data/columns includes ‘playerId’, ‘slotCategoryId’. Only adding ‘slotCategoryId’ because it directly maps to the free agent data.
    working_roster = add_projected_values(working_roster)  # adds the ESPN projection. Haven’t found this data in the api, so it requires scraping the html.
    working_roster = sort_on_projected(working_roster)
    adjust_web_roster(working_roster)
    return working_roster


def adjust_web_roster(working_roster, dropIds = [], pickupIds = []):
    """Does the adds, drops, and moves on the web page itself."""
    print('Need to drop the following:', dropIds)
    print('Need to pick up the following off the waiver wire:', pickupIds)
    print('Need to perform move actions on the web to match this roster:\n', working_roster)
    # web_action.drop dropIds off the roster
    # web_action.Add pickupIds to the bench
    # Perform move actions until the web matches the working roster
    return 0


def rob_waiver_wire():  # Pick up better players
    pos_ids = {0: 'QB', 2: 'RB', 3: 'RB/WR', 4: 'WR', 6: 'TE', 23: 'FLEX', 17: 'K', 16: 'D/ST', 20: 'Bench', 21: 'IR'}
    drop_ids = []
    pickup_ids = []
    working_roster = rearrange_current_roster()  # returns a optimized working roster that should match the web. May not need the web update, but is good for troubleshooting
    for key in pos_ids:  # Go through each ‘slotCategoryId’
        # Maybe pull bench out separate, so you can consider what sort of bench makeup you want?
        # Does it matter which order you go through the positions?
        working_waiver = top_waiver(key)
        # print('Waiver for key', key, 'is', '\n', working_waiver)
        lowest = -1
        for _ in range(len(working_roster)):  # identify the lowest projected in roster slots for this key
            if working_roster[_][0] == key:
                lowest = _
        print(key, lowest)
        # if working_waiver.iloc[0, 0] > working_roster[lowest][2]:  # compare the projections of the top waiver
        #         print('made it')
                # drop_ids.append(working_roster.lowest_projected[‘slotCategoryId’]['playerId'])  # Add the players to the dropIds list # or instead have the adjust_web_roster function do a compare and build its own list
                # working_roster.lowest_projected(‘slotCategoryId’)[;playerId'] = working_waiver[0]['playerId']  # replace the lowest with this new player playerId
                # Pop the top player off the working_waiver to simulate that it has been picked up
                # pickup_ids.append(working_waiver[0])  # Add the players to the pickupIds list  # or instead have the adjust_web_roster function do a compare and build its own list
        # working _roster = sort_on_projected(working_roster)  # may not need this, depending what it handles (
    adjust_web_roster(working_roster, drop_ids, pickup_ids)


if __name__ == '__main__':
    # table1 = create_roster()
    # print(table1)

    # table1 = boxscores()
    # table1 = create_leaders()
    # top_waiver('QB')

    rob_waiver_wire()