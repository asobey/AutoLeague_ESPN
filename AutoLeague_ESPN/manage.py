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
    priv_data = import_yaml()
    browse = Browse(priv_data)
    parse = Parse()
    logic = Logic()

    parse.table_from_source(browse.team_page_source_from_requests())
    parse.print_table(parse.team)

    parse.waiver_table_from_source(browse.get_waiver_source())
    print(tabulate(parse.waiver['ALL'].nlargest(20, 'PROJ'), headers='keys', tablefmt='psg1'))

    pickup_drop_pairs = logic.optimize_waiver(parse.team, parse.waiver)  # Eventually make this into "functional" programming?
    #[[54325451,254352454],[23454235,54354325]]
    print(pickup_drop_pairs)

    # b.pickup_player(pickup_drop_pairs)  # Action: passes this a list of pairs
    #                                     # (player IDs for the pickup and the drop of pickups from
    #                                     # either free agency or waiver wire)

    parse.table_from_source(browse.team_page_source_from_requests())

    logic.optimize(parse.team)

    print('OPTIMAL POSITION CHART:')
    print(logic.optimal_position_chart)

    logic.optimize_position_table()
    print('OPTIMAL POSITION TABLE:')
    print(tabulate(logic.optimal_position_table, headers='keys', tablefmt='psql'))

    browse.initialize_browser()
    browse.sort_team(parse.team, logic.optimal_position_chart)

