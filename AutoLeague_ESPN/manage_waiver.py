import os
import yaml
from tabulate import tabulate
# program imports

from AutoLeague_ESPN.logic import Logic
# temp imports for waivers
from AutoLeague_ESPN.browse_waiver import Browse
from AutoLeague_ESPN.parse_waiver import Parse
from AutoLeague_ESPN.logic_waiver import Logic


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

    # p.table_from_source(b.driver.page_source)
    # pickup_drop_pairs = logic.optimize(p.team, p.waiver)
    #
    # b.pickup_player(pickup_drop_pairs)  # Action: passes this a list of pairs
    #                                     # (player IDs for the pickup and the drop of pickups from
    #                                     # either free agency or waiver wire)
    #
    # p.table_from_source(b.driver.page_source)
    # logic.optimize(p.team)
    # logic.optimize_position_table()
    # b.sort_team(p.team, logic.optimal_position_chart)


