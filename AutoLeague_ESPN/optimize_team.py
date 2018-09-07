import pandas as pd
from tabulate import tabulate
import AutoLeague_ESPN.team_table_parse as team_table_parse
import AutoLeague_ESPN.browser_functions as browser_functions

POSITIONS = ['QB', 'K', 'D/ST', 'TE', 'RB', 'WR']
SINGLE_SPOT_POSITIONS = ['QB', 'K', 'D/ST']
MULTI_SPOT_POSITIONS = ['TE', 'RB', 'WR']

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

def make_team_dic(table, positions):
    team_dic = {}
    for pos in positions:
        pos_true = table.index[table['POS'].str.contains(pos)].values  # list of true values by row number
        #print(pos + ' : ' + str(pos_true))
        team_dic[pos] = table.loc[pos_true]
        #print(tabulate(team_dic[pos], headers='keys', tablefmt='psql'))
    return team_dic

def rank_team_dic(t_dic, rank_by):
    if rank_by == 'ESPN':
        return rank_team_dic_by_ESPN(t_dic)

def rank_team_dic_by_ESPN(t_dic):
    rank_dic = {}
    for pos in t_dic:

        try:
            rank_dic[pos] = t_dic[pos].sort_values('PROJ', ascending=False)
            #print(tabulate(rank_dic[pos], headers='keys', tablefmt='psql'))
        except:
            print('FAILED!!!!!!!!!!!!!!!!!!!!!!')
            print('at: ' + str(pos))
    return rank_dic


def add_multi_pos_chart(r_dic):
    '''This function combined the remaining (not top 2 in positions) WR/RB/TE into two groups: best WR/RB and best remainder'''
    r_dic['REMAINDER'] = r_dic['RB'].iloc[2:].append(r_dic['WR'].iloc[2:]).append(r_dic['TE'].iloc[1:])
    #print(r_dic['REMAINDER'])
    r_dic['REMAINDER'] = r_dic['REMAINDER'].sort_values('PROJ', ascending=False)
    print('REMAINDER:')
    print(tabulate(r_dic['REMAINDER'], headers='keys', tablefmt='psql'))

    #print(r_dic['REMAINDER']['POS'].iloc[0])
    if r_dic['REMAINDER']['POS'].iloc[0] == 'TE':
        r_dic['RB/WR'] = r_dic['REMAINDER'].iloc[1]
        r_dic['FLEX'] = r_dic['REMAINDER'].iloc[0]
    else:
        r_dic['RB/WR'] = r_dic['REMAINDER'].iloc[0, :]
        r_dic['FLEX'] = r_dic['REMAINDER'].iloc[0, :]
    print('RB/WR:')
    print(tabulate(r_dic['RB/WR'], headers='keys', tablefmt='psql'))
    print('FLEX:')
    print(tabulate(r_dic['FLEX'], headers='keys', tablefmt='psql'))
    return r_dic


def optimal_position_chart(ranked_dic):
    opt_pos_chart = {0:'',1:'',2:'',3:'',4:'',5:'',6:'',7:'',8:'',14:''}
    #                QB   RB1  RB2  RB/WR WR1 WR2  TE   D/ST K    FLEX
    #print(ranked_dic['QB']['ID'][0])
    opt_pos_chart[0] = ranked_dic['QB']['ID'].iloc[0]
    opt_pos_chart[1] = ranked_dic['RB']['ID'].iloc[0]
    opt_pos_chart[2] = ranked_dic['RB']['ID'].iloc[1]
    opt_pos_chart[4] = ranked_dic['WR']['ID'].iloc[0]
    opt_pos_chart[5] = ranked_dic['WR']['ID'].iloc[1]
    opt_pos_chart[6] = ranked_dic['TE']['ID'].iloc[0]
    opt_pos_chart[7] = ranked_dic['D/ST']['ID'].iloc[0]
    opt_pos_chart[8] = ranked_dic['K']['ID'].iloc[0]
    opt_pos_chart[3] = ranked_dic['RB/WR']['ID'][0]
    opt_pos_chart[14] = ranked_dic['FLEX']['ID'][0]
    return opt_pos_chart


if __name__ == '__main__':
    source_file_locations = '..\\offline_webpages\\'
    source_file_name = 'front_page_source'

    team_table = team_table_parse.create_team_table(source_file_locations, source_file_name)
    team_table_parse.print_table(team_table)

    #print(team_table.sort_values('PROJ', ascending=False))

    team_dic = make_team_dic(team_table, POSITIONS)

    ranked_dic = rank_team_dic(team_dic, 'ESPN')

    for pos in POSITIONS:
        print(pos + ': UNRANKED TABLE')
        print(tabulate(team_dic[pos], headers='keys', tablefmt='psql'))
        print(pos + ': RANKED TABLE')
        try:
            print(tabulate(ranked_dic[pos], headers='keys', tablefmt='psql'))
        except:
            pass

    new_ranked_dic = add_multi_pos_chart(ranked_dic)


    optimal_position_chart = optimal_position_chart(new_ranked_dic)

    print('OPTIMAL POSITION CHART:')
    print(optimal_position_chart)




    # top_singles = rank_single_spot_pos(team_table)
    #
    # for pos in multi_spot_positions:
    #     pos_true = table.index[table['POS'].str.contains(pos)].values  # list of true values
    #     if len(pos_true) == 0:
    #         raise ValueError('Position not filled!')
    #     elif len(pos_true) == 1:
    #         raise ValueError('Only 1 in position. Not fully filled!')
    #     else:
    #         if pos == 'RB' or pos == 'WR':
    #             ranking = rank_by_pos(team_table, pos_true)
    #             arrange_top_two(pos, ranking)

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