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
    b = Browse(priv_data)
    p = Parse()
    if priv_data['save_offline']:  # If True save page_source offline
        b.save_source()
        p.table_from_file(priv_data)
    else:  # Else don't save
        p.table_from_source(b.driver.page_source)
    p.print_table()

    logic = Logic()
    logic.optimize(p.team)

    print('OPTIMAL POSITION CHART:')
    print(logic.optimal_position_chart)

    logic.optimize_position_table()
    print('OPTIMAL POSITION TABLE:')
    print(tabulate(logic.optimal_position_table, headers='keys', tablefmt='psql'))

    b.sort_team(p.team, logic.optimal_position_chart)
