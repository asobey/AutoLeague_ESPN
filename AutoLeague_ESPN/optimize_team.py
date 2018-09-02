import pandas as pd
from tabulate import tabulate
import AutoLeague_ESPN.team_table_parse as team_table_parse
import AutoLeague_ESPN.browser_functions as browser_functions

positions = ['QB', 'K', 'D/ST', 'TE', 'RB', 'WR']
single_spot_positions = ['QB', 'K', 'D/ST']
multi_spot_positions = ['TE', 'RB', 'WR']

def optimize(file_location, file_name):

    table = team_table_parse.create_team_table(file_location + file_name)

def player_value(_table, pos_index):
    return _table['PROJ'][pos_index]


def rank_by_pos(table, pos_indexes):
    """ Take the table roster and rank players"""

    print()
    #for i in pos_indexes:
    #   print(table['PLAYER'][i] + ': \t\t\t' + player_value(team_table, i))
    rank_df = table[['PLAYER', 'PROJ']].iloc[pos_indexes]
    print(rank_df)
    print('sorting by PROJ.....')
    #print(type(table['PROJ'][5]))
    rank_df = rank_df.sort_values('PROJ', ascending=False)
    print(rank_df)
    return rank_df

def arrange_top_two(_pos, ranking):
    print(pos)
    ranking['pos_index'] = ranking.index
    print(ranking.iloc[0]['pos_index'])
    if pos == 'RB':
        pass

def rank_single_spot_pos(table):
    top_singles = {'QB': '', 'K': '', 'D/ST': ''}
    top_singles = {'QB': 0, 'K': 9, 'D/ST': 8}  # table row of position

    for pos in top_singles.keys():  # loop thru each position
        print('Optimizing single spot positions: ' + pos + '\'s .........', end=' ')
        pos_true = table.index[table['POS'].str.contains(pos)].values  # list of true values by row number
        print(table['PLAYER'][pos_true])
        if pos in single_spot_positions:
            if len(pos_true) == 0:
                raise ValueError('Position not filled!')
            elif len(pos_true) == 1:
                print('Only 1 ' + pos + ' on roster.')
                if top_singles[pos] != pos_true:
                    browser_functions.move_to_here(table['ID'][pos_true[0]], top_singles[pos])

            else:
                pass

    for x in top_singles.values(): #make sure the single_pos_dictionary is complete before returning
        if x == '':
            raise ValueError('top_singles not complete!')

    return top_singles

if __name__ == '__main__':
    source_file_locations = '..\\offline_webpages\\'
    source_file_name = 'front_page_source'

    team_table = team_table_parse.create_team_table(source_file_locations, source_file_name)
    team_table_parse.print_table(team_table)

    table = team_table # Used temporarily

    top_singles = rank_single_spot_pos(team_table)

    for pos in multi_spot_positions:
        pos_true = table.index[table['POS'].str.contains(pos)].values  # list of true values
        if len(pos_true) == 0:
            raise ValueError('Position not filled!')
        elif len(pos_true) == 1:
            raise ValueError('Only 1 in position. Not fully filled!')
        else:
            if pos == 'RB' or pos == 'WR':
                ranking = rank_by_pos(team_table, pos_true)
                arrange_top_two(pos, ranking)

"""
Logic:

1) Take Single Positions, and fill with best player
    -throw error if no single position available.
2) Take Multiple Positions, and fill by rank:
    -Rank WR
    -Rank RB
    -Rank TE
    -Use Top 2 WR, 2 RB, 1 TE into positions.
    -Top 1 RB/WR for RB/WR slot
    -Top Remaining or FLEX
    

"""