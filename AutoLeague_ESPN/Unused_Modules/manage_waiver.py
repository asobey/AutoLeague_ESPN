import os
import yaml
from tabulate import tabulate
# program imports

# temp imports for waivers
from AutoLeague_ESPN.browse import Browse
from AutoLeague_ESPN.parse import Parse
from AutoLeague_ESPN.Unused_Modules.logic_waiver import Logic


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
    b = Browse(priv_data)
    p = Parse()
    logic = Logic()

    p.table_from_source(b.get_team_page_source())
    p.waiver_table_from_source(b.get_waiver_source())

    # pickup_drop_pairs = logic.optimize(p.team, p.waiver)  # Eventually make this into "functional" programming?
    #
    # b.pickup_player(pickup_drop_pairs)  # Action: passes this a list of pairs
    #                                     # (player IDs for the pickup and the drop of pickups from
    #                                     # either free agency or waiver wire)
    #
    # p.table_from_source(b.driver.page_source)

    logic.optimize(p.team)
    print('OPTIMAL POSITION CHART:')
    print(logic.optimal_position_chart)

    logic.optimize_position_table()
    print('OPTIMAL POSITION TABLE:')
    print(tabulate(logic.optimal_position_table, headers='keys', tablefmt='psql'))

    b.initialize_browser()
    b.sort_team(p.team, logic.optimal_position_chart)


