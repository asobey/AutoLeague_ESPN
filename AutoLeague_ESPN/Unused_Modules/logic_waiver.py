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

    def rob_waiver_wire(self):  # Pick up better players
        pos_ids = {0: 'QB', 2: 'RB', 3: 'RB/WR', 4: 'WR', 6: 'TE', 23: 'FLEX', 17: 'K', 16: 'D/ST', 20: 'Bench',
                   21: 'IR'}
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
        print('Need to drop the following:', drop_ids)
        print('Need to pick up the following off the waiver wire:', pickup_ids)
        print('Need to perform move actions on the web to match this roster:\n', working_roster)

    def optimize(self, team_table):
        """Single function calls several others to optimize team"""
        self.team_table = team_table
        self.make_team_dic()
        self.rank_team_dic('ESPN')
        self.add_multi_pos_chart()
        self.optimize_position_chart()
        self.handle_multi_spot_anomoly()

    def make_team_dic(self):
        """Make a dictionary of the team_table separated by position"""
        for position in self.POSITIONS:  # Each position gets it's own table
            pos_true = self.team_table.index[self.team_table['POS'].str.contains(position)].values  # list of true
            # values by row number
            self.team_dic[position] = self.team_table.loc[pos_true]

    def rank_team_dic(self, rank_by):
        """Takes team_dic and ranks players by position depending on method (i.e. ESPN, Yahoo, ect."""
        if rank_by == 'ESPN':
            self.rank_team_dic_by_espn()
        elif rank_by == 'Yahoo':
            raise ValueError('This ranking method does not exist yet!')
        else:
            raise ValueError('No ranking method selected for players')

    def rank_team_dic_by_espn(self):
        """Takes team_dic and ranks players by position according to ESPN projections"""
        for position in self.team_dic:
            try:
                self.ranked_dic[position] = self.team_dic[position].sort_values('PROJ', ascending=False)
                print(position + ': RANKED TABLE')
                print(tabulate(self.ranked_dic[position], headers='keys', tablefmt='psql'))
            except ValueError:
                print('FAILED!!!!!!!!!!!!!!!!!!!!!!...at: ' + str(position))
                print(tabulate(self.ranked_dic[position], headers='keys', tablefmt='psql'))

    def rank_dict(self, dict, rank_by):
        """Takes team_dic and ranks players by position depending on method (i.e. ESPN, Yahoo, ect."""
        if rank_by == 'ESPN':
            return self.rank_dict_by_espn(dict)
        elif rank_by == 'Yahoo':
            raise ValueError('This ranking method does not exist yet!')
        else:
            raise ValueError('No ranking method selected for players')

    def rank_dict_by_espn(dict):
        """Takes team_dic and ranks players by position according to ESPN projections"""
        for position in dict:
            try:
                dict[position] = dict[position].sort_values('PROJ', ascending=False)
                print(position + ': RANKED TABLE')
                print(tabulate(dict[position], headers='keys', tablefmt='psql'))
                return dict
            except ValueError:
                print('FAILED!!!!!!!!!!!!!!!!!!!!!!...at: ' + str(position))
                print(tabulate(dict[position], headers='keys', tablefmt='psql'))

    def add_multi_pos_chart(self):
        """This function combined the remaining (not top 2 in positions) WR/RB/TE into two groups: best WR/RB and best
        remainder"""
        r_dic = self.ranked_dic
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
        self.ranked_dic_w_multispot = r_dic

    def optimize_position_chart(self):
        """Create dictionary of optimized position chart"""
        self.optimal_position_chart[0] = self.ranked_dic_w_multispot['QB']['ID'].iloc[0]
        self.optimal_position_chart[1] = self.ranked_dic_w_multispot['RB']['ID'].iloc[0]
        self.optimal_position_chart[2] = self.ranked_dic_w_multispot['RB']['ID'].iloc[1]
        self.optimal_position_chart[3] = self.ranked_dic_w_multispot['RB/WR']['ID'].iloc[0]
        self.optimal_position_chart[4] = self.ranked_dic_w_multispot['WR']['ID'].iloc[0]
        self.optimal_position_chart[5] = self.ranked_dic_w_multispot['WR']['ID'].iloc[1]
        self.optimal_position_chart[6] = self.ranked_dic_w_multispot['TE']['ID'].iloc[0]
        self.optimal_position_chart[14] = self.ranked_dic_w_multispot['FLEX']['ID'].iloc[0]
        self.optimal_position_chart[7] = self.ranked_dic_w_multispot['D/ST']['ID'].iloc[0]
        self.optimal_position_chart[8] = self.ranked_dic_w_multispot['K']['ID'].iloc[0]

    def handle_multi_spot_anomoly(self):
        """The ESPN website does not allow for player in RB1 slot to move to RB1 and vice-versa. This is also true for WR1
        and WR2. This function can only handle leagues with 2 RBs and/or 2 WR2. Two QB or any other multi spot positions
        with throw an exception at the end."""

        # Only need to check for RB1(1) and WR1(3). Error cannot occur with RB2(2) or WR2(4) positions
        for key, value in self.optimal_position_chart.items():
            if key == 1 and self.team_table['HERE'].loc[self.team_table['ID'] == value].item() == 2:
                temp_id = self.optimal_position_chart[1]
                self.optimal_position_chart[1] = self.optimal_position_chart[2]
                self.optimal_position_chart[2] = temp_id
            if key == 3 and self.team_table['HERE'].loc[self.team_table['ID'] == value].item() == 4:
                temp_id = self.optimal_position_chart[3]
                self.optimal_position_chart[3] = self.optimal_position_chart[4]
                self.optimal_position_chart[4] = temp_id

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


if __name__ == '__main__':
    from AutoLeague_ESPN.parse import Parse
    import yaml
    import os

    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        private_data = yaml.load(_private)
    p = Parse()
    p.table_from_file(private_data)
    p.print_table(p.team)

    logic = Logic()
    logic.optimize(p.team)

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