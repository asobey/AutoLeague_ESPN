import os
import yaml
from tabulate import tabulate
# program imports

from AutoLeague_ESPN.logic import Logic
# temp imports for waivers
from AutoLeague_ESPN.browse_waiver import Browse
from AutoLeague_ESPN.parse_waiver import Parse


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

    p.top_waiver(b.get_waiver_source())
    # print(tabulate.tabulate(p.waiver.values(), headers='keys', tablefmt='psgl'))
    # print(tabulate.tabulate(p.waiver.values(), headers='keys', tablefmt="orgtbl"))

    # logic = Logic()
    # logic.optimize(p.team)
    #
    # print('OPTIMAL POSITION CHART:')
    # print(logic.optimal_position_chart)
    #
    # logic.optimize_position_table()
    # print('OPTIMAL POSITION TABLE:')
    # print(tabulate(logic.optimal_position_table, headers='keys', tablefmt='psql'))
    #
    # b.sort_team(p.team, logic.optimal_position_chart)
