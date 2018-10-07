from tabulate import tabulate
import pandas as pd


class Logic(object):

    def __init__(self):
        self.POSITIONS = ['QB', 'K', 'D/ST', 'TE', 'RB', 'WR']
        self.team_dic = {}
        self.ranked_dic = {}
        self.ranked_dic_w_multispot = {}
        self.optimal_position_chart = {}
        self.team_table = pd.DataFrame()
        self.optimal_position_table = pd.DataFrame()

    def optimize_team(self, team_table):
        """Single function calls several others to optimize team"""
        self.team_table = team_table
        self.team_dic = self.make_team_dic(team_table, self.POSITIONS)
        ranked_dic = self.rank_team_dic(self.team_dic, 'ESPN')
        self.ranked_dic_w_multispot = self.add_multi_pos_chart(ranked_dic)
        opt_pos_chart = self.optimize_position_chart(self.ranked_dic_w_multispot)
        self.optimal_position_chart = self.handle_multi_spot_anomoly(team_table, opt_pos_chart)

    @staticmethod
    def make_team_dic(team_table, positions):
        """Make a dictionary of the team_table separated by position"""
        team_dic = {}
        for position in positions:  # Each position gets it's own table
            pos_true = team_table.index[team_table['POS'].str.contains(position)].values  # list of true
            # values by row number
            team_dic[position] = team_table.loc[pos_true]
        return team_dic

    def rank_team_dic(self, team_dic, rank_by):
        """Takes team_dic and ranks players by position depending on method (i.e. ESPN, Yahoo, ect."""
        if rank_by == 'ESPN':
            return self.rank_team_dic_by_espn(team_dic)
        elif rank_by == 'Yahoo':
            raise ValueError('This ranking method does not exist yet!')
        else:
            raise ValueError('No ranking method selected for players')

    @staticmethod
    def rank_team_dic_by_espn(team_dic):
        """Takes team_dic and ranks players by position according to ESPN projections"""
        ranked_dic = {}
        for position in team_dic:
            try:
                ranked_dic[position] = team_dic[position].sort_values('PROJ', ascending=False)
                print(position + ': RANKED TABLE')
                print(tabulate(ranked_dic[position], headers='keys', tablefmt='psql'))
            except ValueError:
                print('FAILED!!!!!!!!!!!!!!!!!!!!!!...at: ' + str(position))
                print(tabulate(ranked_dic[position], headers='keys', tablefmt='psql'))
        return ranked_dic

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
    def optimize_position_chart(ranked_dic_w_multispot):
        """Create dictionary of optimized position chart. This method need to be more flexible with different teams"""
        optimal_position_chart = {}
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

    def handle_multi_spot_anomoly(self, team_table, optimal_position_chart):
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

    def optimize_position_table(self):
        """Turn Optimal Position Chart into a easy to read table."""
        first = True
        for key, value in self.optimal_position_chart.items():
            if first:
                self.optimal_position_table = self.team_table.loc[self.team_table['ID'] == value]
                first = False
            else:
                self.optimal_position_table = self.optimal_position_table.append(self.team_table.loc[self.team_table[
                                                                                                        'ID'] == value])
    def optimize_waiver(self, team_table, waiver_table):
        """something"""
        player_pairs = [[16724, 5536], [23454235, 54354325]]  #temp assignment as an example
        #self.make_team_dic()
        #self.rank_team_dic('ESPN')
        # self.add_multi_pos_chart()
        # self.optimize_position_chart()
        # self.handle_multi_spot_anomoly()

        # for position in self.POSITIONS:

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

        return player_pairs

if __name__ == '__main__':
    from AutoLeague_ESPN.parse import Parse
    import yaml
    import os

    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        private_data = yaml.load(_private)
    parse = Parse()
    parse.table_from_file(private_data)
    parse.print_table(parse.team)

    logic = Logic()
    logic.optimize_team(parse.team)

    print('OPTIMAL POSITION CHART:')
    print(logic.optimal_position_chart)

    logic.optimize_position_table()
    print(tabulate(logic.optimal_position_table, headers='keys', tablefmt='psql'))

"""
Logic:

-Take Top 
    -QB
    -2X RB
    -2X WR
    -TE
    -D/ST
    -K
    -Remaining WR/RB
    -Remaining WR/RB/TE
    
*Change order based on day played to add flexibility
"""