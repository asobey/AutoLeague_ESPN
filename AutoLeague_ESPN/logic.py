from tabulate import tabulate
import pandas as pd


class Logic(object):

    def __init__(self):
        self.POSITIONS = ['QB', 'K', 'D/ST', 'TE', 'RB', 'WR']
        self.ranked_dic = {}
        self.ranked_dic_w_multispot = {}
        self.optimal_position_chart = {}
        self.team_table = pd.DataFrame()
        self.optimal_position_table = pd.DataFrame()

    def optimize_team(self, team_table, rank_by):
        """Single function calls several others to optimize team"""
        self.team_table = team_table
        team_dic = self.make_team_dic(team_table, self.POSITIONS)
        ranked_dic = self.rank_team_dic(team_dic, rank_by)
        self.ranked_dic_w_multispot = self.add_multi_pos_chart(ranked_dic)
        _optimal_position_chart = self.optimize_position_chart(self.ranked_dic_w_multispot)
        self.optimal_position_chart = self.handle_multi_spot_anomoly(team_table, _optimal_position_chart)
        return self.optimal_position_chart

    @staticmethod
    def make_team_dic(team_table, positions):
        """Make a dictionary of the team_table separated by position"""
        team_dictionary = {}
        for position in positions:  # Each position gets it's own table
            pos_true_mask = team_table.index[team_table['POS'].str.contains(position)].values  # list of true
            # values by row number
            team_dictionary[position] = team_table.loc[pos_true_mask]
        return team_dictionary

    def rank_team_dic(self, team_dictionary, rank_by):
        """Takes team_dic and ranks players by position depending on method (i.e. ESPN, Yahoo, ect."""
        if rank_by == 'ESPN_PROJ':
            return self.rank_team_dic_by_column(team_dictionary, 'PROJ')
        elif rank_by == 'INTERNAL':
            return self.rank_team_dic_by_column(team_dictionary, 'INTERNAL')
        elif rank_by == 'Yahoo_PROJ':
            raise ValueError('This ranking method does not exist yet!')
        else:
            raise ValueError('No ranking method selected for players')

    @staticmethod
    def rank_team_dic_by_column(team_dictionary, rank_by_column):
        """Takes team_dic and ranks players by position according to ESPN projections"""
        ranked_dictionary = {}
        for position in team_dictionary:
            try:
                ranked_dictionary[position] = team_dictionary[position].sort_values(rank_by_column, ascending=False)
                print(position + ': RANKED TABLE BY COLUMN: ' + rank_by_column)
                print(tabulate(ranked_dictionary[position].head(10), headers='keys', tablefmt='psql'))
            except ValueError:
                print('FAILED!!!!!!!!!!!!!!!!!!!!!!...at: ' + str(position))
                print(tabulate(ranked_dictionary[position], headers='keys', tablefmt='psql'))
        return ranked_dictionary

    @staticmethod
    def add_multi_pos_chart(ranked_dic):
        """This function combined the remaining (not top 2 in positions) WR/RB/TE into two groups: best WR/RB and best
        remainder"""
        r_dic = ranked_dic  # Use shortened form to fit code in readable lines
        r_dic['REMAINDER'] = r_dic['RB'].iloc[2:].append(r_dic['WR'].iloc[2:]).append(r_dic['TE'].iloc[1:])

        r_dic['REMAINDER'] = r_dic['REMAINDER'].sort_values('PROJ', ascending=False)
        print('REMAINDER:')
        print(tabulate(r_dic['REMAINDER'], headers='keys', tablefmt='psql'))

        if r_dic['REMAINDER']['POS'].iloc[0] == 'TE':
            r_dic['RB/WR'] = r_dic['REMAINDER'].drop(r_dic['REMAINDER'].index[2:]).drop(r_dic['REMAINDER'].index[0])
            r_dic['FLEX'] = r_dic['REMAINDER'].drop(r_dic['REMAINDER'].index[1:])
        else:
            r_dic['RB/WR'] = r_dic['REMAINDER'].drop(r_dic['REMAINDER'].index[1:])
            r_dic['FLEX'] = r_dic['REMAINDER'].drop(r_dic['REMAINDER'].index[2:]).drop(r_dic['REMAINDER'].index[0])
        print('RB/WR:')
        print(tabulate(r_dic['RB/WR'], headers='keys', tablefmt='psql'))
        print('FLEX:')
        print(tabulate(r_dic['FLEX'], headers='keys', tablefmt='psql'))
        return r_dic

    @staticmethod
    def optimize_position_chart(ranked_dic_w_multispot):  # chart is defined as dictionary pairs
        """Create dictionary of optimized position chart. This method need to be more flexible with different teams"""
        optimal_position_chart = {}  # Going to ignore rewrite recomendation as following code reads cleaner
        optimal_position_chart[0] = ranked_dic_w_multispot['QB']['ID'].iloc[0]
        optimal_position_chart[1] = ranked_dic_w_multispot['RB']['ID'].iloc[0]
        optimal_position_chart[2] = ranked_dic_w_multispot['RB']['ID'].iloc[1]
        optimal_position_chart[3] = ranked_dic_w_multispot['RB/WR']['ID'].iloc[0]
        optimal_position_chart[4] = ranked_dic_w_multispot['WR']['ID'].iloc[0]
        optimal_position_chart[5] = ranked_dic_w_multispot['WR']['ID'].iloc[1]
        optimal_position_chart[6] = ranked_dic_w_multispot['TE']['ID'].iloc[0]
        optimal_position_chart[14] = ranked_dic_w_multispot['FLEX']['ID'].iloc[0]
        optimal_position_chart[7] = ranked_dic_w_multispot['D/ST']['ID'].iloc[0]
        optimal_position_chart[8] = ranked_dic_w_multispot['K']['ID'].iloc[0]
        return optimal_position_chart

    @staticmethod
    def handle_multi_spot_anomoly(team_table, optimal_position_chart):
        """The ESPN website does not allow for player in RB1 slot to move to RB1 and vice-versa. This is also true for WR1
        and WR2. This function can only handle leagues with 2 RBs and/or 2 WR2. Two QB or any other multi spot positions
        with throw an exception at the end."""

        # Only need to check for RB1(1) and WR1(3). Error cannot occur with RB2(2) or WR2(4) positions
        for key, value in optimal_position_chart.items():
            if key == 1 and team_table['HERE'].loc[team_table['ID'] == value].item() == 2:
                temp_id = optimal_position_chart[1]
                optimal_position_chart[1] = optimal_position_chart[2]
                optimal_position_chart[2] = temp_id
            if key == 3 and team_table['HERE'].loc[team_table['ID'] == value].item() == 4:
                temp_id = optimal_position_chart[3]
                optimal_position_chart[3] = optimal_position_chart[4]
                optimal_position_chart[4] = temp_id
        return optimal_position_chart

    @staticmethod
    def table_from_chart(team_table, chart):  # chart is defined as dictionary pairs
        """Turn Optimal Position Chart into a easy to read table."""
        optimal_position_table = pd.DataFrame()
        first = True
        for key, value in chart.items():
            if first:
                optimal_position_table = team_table.loc[team_table['ID'] == value]
                first = False
            else:
                optimal_position_table = optimal_position_table.append(team_table.loc[team_table['ID'] == value])
        return optimal_position_table

    @staticmethod
    def add_internal_rank(table):
        # Internal Rank Weightings
        prk_wt = 50
        prk_adj = 124
        last_wt = 1
        proj_wt = 5
        no_proj_wt = .5  # if no proj then average used with this weighting
        st_wt = 1
        own_wt = 1
        internal_rank = [0] * len(table)  # Start by filling all rows with 0
        table['INTERNAL'] = internal_rank
        for i in table.index:
            last = table['LAST'][i]
            if last != -1:
                pass
            elif last == -1 and table['AVG'][i] != -1:
                last = table['AVG'][i]
            elif last == -1 and table['AVG'][i] == -1:
                last = 0  # No AVG or LAST so assign player. Either early in the season or player hasn't played much
            else:
                last = 0
            proj = table['PROJ'][i]
            if proj != -1:
                pass
            elif proj == -1 and table['AVG'][i] != -1:
                proj = table['AVG'][i] * no_proj_wt
            elif proj == -1 and table['AVG'][i] == -1:
                proj = 0  # No AVG or LAST so assign player. Either early in the season or player hasn't played much
            else:
                proj = 0
            table.loc[i, 'INTERNAL'] = (prk_adj-table['PRK'][i])/prk_adj*prk_wt + last*last_wt + proj*proj_wt + \
                                       table['%ST'][i]*st_wt + table['%OWN'][i]*own_wt
        return table

    def optimize_waiver(self, team_table, waiver_table, optimize_by='INTERNAL', threshold=1.01):
        """Single function calls several others to find best waiver players and compare to current roster"""
        player_pairs = [[16724, 5536], [23454235, 54354325]]  #temp assignment as an example

        worst_player_dictionary, worst_player_chart = self.worst_players_on_team(team_table, optimize_by)
        worst_player_table = self.table_from_chart(team_table, worst_player_chart)
        print('WORST PLAYER TABLE:')
        print(tabulate(worst_player_table, headers='keys', tablefmt='psql'))

        waiver_best_dictionary, waiver_best_table = self.best_players_on_waiver(waiver_table, optimize_by)
        waiver_best_table = self.table_from_chart(waiver_table, waiver_best_table)
        print('BEST WAIVER TABLE:')
        print(tabulate(waiver_best_table, headers='keys', tablefmt='psql'))

        trade_list_columns = ['pos', 'delta', 'drop_id', 'pickup_id']
        trade_list = pd.DataFrame()
        for position in self.POSITIONS:
            if worst_player_dictionary[position]['INTERNAL'].values[0]*threshold < \
                    waiver_best_dictionary[position]['INTERNAL'].values[0]:
                delta = waiver_best_dictionary[position]['INTERNAL'].values[0] - \
                        worst_player_dictionary[position]['INTERNAL'].values[0]*threshold
                drop_id = worst_player_dictionary[position]['ID'].values[0]
                pickup_id = waiver_best_dictionary[position]['ID'].values[0]
                trade_list = trade_list.append(pd.DataFrame([[position, delta, drop_id, pickup_id]], columns=trade_list_columns))
                #print(trade_list, headers='keys', tablefmt='psql'))
                print('\033[96m' + '==================================================================================='
                                   '======================================================================' + '\033[0m')
                print('RECOMMENDED ' + position + ' TRADE:')
                print(tabulate(worst_player_dictionary[position], headers='keys', tablefmt='psql'))
                print('for...')
                print(tabulate(waiver_best_dictionary[position], headers='keys', tablefmt='psql'))
        trade_list = trade_list.sort_values('delta', ascending=False)
        print('TRADE LIST")')
        print(tabulate(trade_list, headers='keys', tablefmt='psql'))
        # if waiver QBs is better than the QB roster slot
        #     add waiver qb to pickup list
        # if waiver Ks is better than the K roster slot
        #     add waiver K to pickup list

        # if waiver TEs is better than the TE roster slots
        #     if old TE is better than FLEX
        #         if old FLEX
        #     else compare waiver TE to all roster FLEX
        #     add waiver TE to pickup list

        # Bench approach:
        #   Max 1 QB only if main is Q, or D, or upcoming BYE
        #   Max 1 K only if main is Q, or D, or upcoming BYE
        #   Max 1 D/ST ... must choose this one with a heavier ranking based on forward OPRK
        #   Max 2 TE
        #   Max 3 RB
        #   Max 3 WR --WR are most valuable FLEX
        return trade_list

    def worst_players_on_team(self, team_table, rank_by):
        team_dic = self.make_team_dic(team_table, self.POSITIONS)
        opt_pos_dic_internal = self.rank_team_dic(team_dic, rank_by)
        worst_player_dictionary = {}
        worst_player_chart = {}
        for df in opt_pos_dic_internal:
            worst_player_chart[df] = opt_pos_dic_internal[df].tail(1)['ID'].values[0]
            worst_player_dictionary[df] = opt_pos_dic_internal[df].tail(1)
            print(tabulate(opt_pos_dic_internal[df].tail(1), headers='keys', tablefmt='psql'))
        print(worst_player_chart)
        return worst_player_dictionary, worst_player_chart

    def best_players_on_waiver(self, waiver_table, optimize_by):
        waiver_best_dictionary = {}
        waiver_best_chart = {}
        waiver_dictionary = self.make_team_dic(waiver_table, self.POSITIONS)
        ranked_waiver_dictionary = self.rank_team_dic(waiver_dictionary, optimize_by)
        for df in ranked_waiver_dictionary:
            #print('WAIVER WIRE BEST: ' + df)
            #print(tabulate(ranked_waiver_dictionary[df].head(5), headers='keys', tablefmt='psql'))
            waiver_best_chart[df] = ranked_waiver_dictionary[df].head(1)['ID'].values[0]
            waiver_best_dictionary[df] = ranked_waiver_dictionary[df].head(1)

        print(waiver_best_chart)
        return waiver_best_dictionary, waiver_best_chart


if __name__ == '__main__':
    from AutoLeague_ESPN.browse import Browse
    from AutoLeague_ESPN.parse import Parse
    import yaml
    import os

    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        private_data = yaml.load(_private)
    browse = Browse(private_data)
    parse = Parse()
    logic = Logic()

    print('\033[96m' + '==========+++++++++++++++++============' + '\033[0m')
    print('\033[96m' + '==========TEAM MANAGEMENT============' + '\033[0m')
    print('\033[96m' + '==========+++++++++++++++++============' + '\033[0m')

    team = parse.table_from_source(browse.get_team_page_source())
    team = logic.add_internal_rank(team)
    parse.print_table(team)

    opt_pos_chart = logic.optimize_team(team, 'ESPN_PROJ')
    print('OPTIMAL POSITION CHART:')
    print(opt_pos_chart)

    opt_pos_table = logic.table_from_chart(team, opt_pos_chart)
    print(tabulate(opt_pos_table, headers='keys', tablefmt='psql'))

    print('\033[96m' + '==========+++++++++++++++++============' + '\033[0m')
    print('\033[96m' + '==========WAIVER MANAGEMENT============' + '\033[0m')
    print('\033[96m' + '==========+++++++++++++++++============' + '\033[0m')
    waiver = parse.waiver_table_from_source(browse.get_waiver_source())

    waiver = logic.add_internal_rank(waiver)
    print('WAIVER TABLE')
    parse.print_table(waiver.head(40))

    logic.optimize_waiver(team, waiver, 'INTERNAL', 1.05)
