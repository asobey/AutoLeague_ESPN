# This file will save off stats, so they can be used later to refine the ranking algorithms

import yaml
import os
from tabulate import tabulate
import datetime

from AutoLeague_ESPN.browse import Browse
from AutoLeague_ESPN.parse import Parse

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

    p.waiver_table_from_source(b.get_waiver_source('full'))
    print(tabulate(p.waiver['ALL'].nlargest(20, 'PROJ'), headers='keys', tablefmt='psg1'))

    path = '..\\AutoLeague_ESPN'
    p.waiver['ALL'].to_csv(os.path.join(path, datetime.date.today().isoformat() + '_waiver.csv'))  # Save to cvs and pickle
    print('Data for', len(p.waiver['ALL']), 'players was stored to the CSV file in', path)
