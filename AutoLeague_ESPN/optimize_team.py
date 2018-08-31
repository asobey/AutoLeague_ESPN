import pandas as pd
from tabulate import tabulate
import pandas_bs4_table_parse

positions = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']

def optimize(file_location, file_name):

    table = pandas_bs4_table_parse.create_team_table(file_location + file_name)

def rank_by_pos(table, pos_indexes):
    print()
    #for i in pos_indexes:
    #   print(table['PLAYER'][i] + ': \t\t\t' + player_value(team_table, i))
    rank_db = table[['PLAYER', 'PROJ']].iloc[pos_indexes]
    print(rank_db)
    print('sorting by PROJ.....')
    print(type(table['PROJ'][2]))
    rank_db = rank_db.sort_values(['PROJ'], ascending=False)
    print(rank_db)


def player_value(_table, pos_index):
    return _table['PROJ'][pos_index]


if __name__ == '__main__':
    source_file_locations = '..\\offline_webpages\\'
    source_file_name = 'front_page_source'

    team_table = pandas_bs4_table_parse.create_team_table(source_file_locations, source_file_name)
    pandas_bs4_table_parse.print_table(team_table)

    table = team_table # Used temporarily

    for pos in positions:
        print('Optimizing: ' + pos + ' .........', end=' ')

        pos_true = table.index[table['POS'].str.contains(pos)].values
        if len(pos_true) == 0:
            raise ValueError('Position not filled!')
        elif len(pos_true) == 1:
            print('Only 1 ' + pos + ' on roster. No Changes made')
        else:
            if pos == 'RB':
                #for i in pos_true:
                #    print(team_table['PLAYER'][i] + ': ' + player_value(team_table, i))
                rank_by_pos(team_table, pos_true)
