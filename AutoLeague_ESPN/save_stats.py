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

    full_waiver = p.waiver_table_from_source(b.get_waiver_source(20, 'full'))
    # print(tabulate(full_waiver.nlargest(50, 'PROJ'), headers='keys', tablefmt='psg1'))

    path = '..\\AutoLeague_ESPN'
    full_waiver.to_csv(os.path.join(path, datetime.date.today().isoformat() + '_waiver.csv'))  # Save to cvs and pickle
    print('Data for', len(full_waiver), 'players was stored to the CSV file in', path)

    print('=======ONLY FREE AGENT PLAYERS=============')
    pos_true = full_waiver.index[full_waiver['Waiver Day'].str.contains('FA', na=False)].values
    free_agent_waiver = full_waiver.loc[pos_true]  # This is how to correctly set value in df
    print(tabulate(free_agent_waiver.nlargest(50, 'PROJ'), headers='keys', tablefmt='psg1'))

    print('=======ONLY WAIVER PLAYERS=============')
    pos_true = full_waiver.index[full_waiver['Waiver Day'].str.contains('WA', na=False)].values
    free_waiver = full_waiver.loc[pos_true]  # This is how to correctly set value in df
    print(tabulate(free_waiver.nlargest(50, 'PROJ'), headers='keys', tablefmt='psg1'))