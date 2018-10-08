import os
import yaml
from tabulate import tabulate
# program imports
from AutoLeague_ESPN.browse import Browse
from AutoLeague_ESPN.parse import Parse
from AutoLeague_ESPN.logic import Logic


def import_yaml():
    """This function opens the espn_creds.yaml file and returns its contents as privateData"""
    with open(os.path.join('..\\AutoLeague_ESPN', 'espn_creds.yaml'), 'r') as _private:
        try:
            private_data = yaml.load(_private)
            return private_data
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    priv_data = import_yaml()  # Bring in private credentials
    # Initialize Required Classes
    browse = Browse(priv_data)
    parse = Parse()
    logic = Logic()
    print('\033[96m' + '==========+++++++++++++++++============' + '\033[0m')
    print('\033[96m' + '===========TEAM MANAGEMENT=============' + '\033[0m')
    print('\033[96m' + '==========+++++++++++++++++============' + '\033[0m')
    # Get Current Team
    team = parse.table_from_source(browse.get_team_page_source())
    team = logic.add_internal_rank(team)
    parse.print_table(team)
    # Get current Waiver
    print('\033[96m' + '==========+++++++++++++++++============' + '\033[0m')
    print('\033[96m' + '==========WAIVER MANAGEMENT============' + '\033[0m')
    print('\033[96m' + '==========+++++++++++++++++============' + '\033[0m')
    waiver = parse.waiver_table_from_source(browse.get_waiver_source())
    waiver = logic.add_internal_rank(waiver)
    print('WAIVER TABLE')
    parse.print_table(waiver.head(40))

    # Optimize Team In Logic and Print
    opt_pos_chart = logic.optimize_team(team, 'ESPN_PROJ')
    print('OPTIMAL POSITION CHART:')
    print(opt_pos_chart)
    opt_pos_table = logic.table_from_chart(team, opt_pos_chart)
    print('OPTIMAL POSITION TABLE:')
    print(tabulate(opt_pos_table, headers='keys', tablefmt='psql'))
    browse.initialize_browser()
    browse.sort_team(parse.team, logic.optimal_position_chart)
    # Last argument is threshold (how much better a waiver player must be to trade)
    logic.optimize_waiver(team, waiver, 'INTERNAL', 1.05)
