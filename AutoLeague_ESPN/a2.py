# ---------------------------------------------------------
# Main file for Josh's architecture
# Every day: rob_waiver_wire()  # may be able to use AWS
#

# Pseudo code

import requests
from bs4 import BeautifulSoup
import pandas as pd
import yaml
# import numpy as np
import re
from tabulate import tabulate


with open('espn_creds.yaml', 'r') as _private:
    privateData = yaml.load(_private)    # pulls in the person specific data (teamId, cookies, etc)


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
        slot = slots[position]
        parameters = {'leagueId': privateData['leagueid'], 'teamID': privateData['teamid'],
                      'slotCategoryId': slot, 'avail': 1, 'injury': 2, 'context': 'freeagency',
                      'view': 'overview'}

    df = pd.DataFrame(columns=['Player', 'Opponent', 'Projected', 'OppRank', '%Start', '%Own', '+/-'])

    for si in [0, 50, 100]:
        parameters['startIndex'] = si
        r = requests.get('http://games.espn.com/ffl/freeagency',
                         params=parameters,
                         cookies=cookies)

        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', class_='playerTableTable')
        tdf = pd.read_html(str(table), flavor='bs4')[0]  # returns a list of df's, grab first

        tdf = tdf.iloc[2:, [0, 5, 13, 14, 15, 16, 17]].reset_index(drop=True)  # delete the useless columns
        tdf = add_player_id(tdf, soup)
        tdf.columns = ['Player', 'Opponent', 'Projected', 'OppRank', '%Start', '%Own', '+/-', 'PlayerID']
        df = df.append(tdf, ignore_index=True, sort=False)  # !!!! non-concatenation axis is not aligned. remove the "sort=false" to troubleshoot

    df = df.query('Projected != "--"')
    df['Projected'] = df['Projected'].fillna(0).astype('float')  # !!!! troubleshoot. try  df.loc['Projected'] = df[...
    # df['Player'] = df['Player'].str.split(',').str[0]  # keep just player name
    # print(tabulate(tdf, headers='keys', tablefmt='psg1'))

    return df


def top_waiver(position='none'):
    """this "top" ranking is personal preference. initial setup is based on espn's projection"""

    df = create_waiver(position)
    player = df.nlargest(3, 'Projected')
    # maybe do a reindex or something?
    print(tabulate(player, headers='keys', tablefmt='psg1'))

    return player


def sort_on_projected(roster):
    print('sorting on projected')
    return roster


def rearrange_current_roster():  # eventually add something that fixes for Thursdays
    working_roster = []
    # working_roster = build_roster()  # Builds the working file for the roster. Required data/columns includes ‘playerId’, ‘slotCategoryId’. Only adding ‘slotCategoryId’ because it directly maps to the free agent data.
    # working_roster = add_projected_values(working_roster)  # adds the ESPN projection. Haven’t found this data in the api, so it requires scraping the html.
    working_roster = sort_on_projected(working_roster)
    adjust_web_roster(working_roster)
    return working_roster


def adjust_web_roster(working_roster, dropIds = [], pickupIds = []):
    """Does the adds, drops, and moves on the web page itself."""
    # web_action.drop dropIds off the roster
    # web_action.Add pickupIds to the bench
    # Perform move actions until the web matches the working roster
    return 0


def rob_waiver_wire():  # Pick up better players
    pos_ids = {0: 'QB', 2: 'RB', 3: 'RB/WR', 4: 'WR', 6: 'TE', 23: 'FLEX', 17: 'K', 16: 'D/ST', 20: 'Bench', 21: 'IR'}
    drop_ids = []
    pickup_ids = []
    working_roster = rearrange_current_roster()  # returns a optimized working roster that should match the web. May not need the web update, but is good for troubleshooting
    for key in pos_ids:  # Go through each ‘slotCategoryId’ (maybe pull bench out separate, so you can consider what sort of bench makeup you want?) Does it matter which order you go through the positions?
        print(key)
        #  working_waiver = top_waiver(key)  # check if this should be the slotCategoryId or the string (0 or ‘QB’) (key or value)
        # For j in len(working_roster[‘slotCategoryId’])  # look at each player in that ‘slotCategoryId’ --- needs fixing
            # If working_waiver[0].projected >  working_roster.lowest_projected[‘slotCategoryId’][j]
                    # drop_ids.append(working_roster.lowest_projected[‘slotCategoryId’]['playerId'])  # Add the players to the dropIds list # or instead have the adjust_web_roster function do a compare and build its own list
                    # working_roster.lowest_projected(‘slotCategoryId’)[;playerId'] = working_waiver[0]['playerId']  # replace the lowest with this new player playerId
                    # Pop the top player off the working_waiver to simulate that it has been picked up
                    # pickup_ids.append(working_waiver[0])  # Add the players to the pickupIds list  # or instead have the adjust_web_roster function do a compare and build its own list
        # working _roster = sort_on_projected(working_roster)  # may not need this, depending what it handles (
    adjust_web_roster(working_roster, drop_ids, pickup_ids)