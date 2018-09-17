import os
import yaml
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
    webdriver = Browse(priv_data)
    parser = Parse()
    webdriver.save_source()
    parser.table_from_file(priv_data)
    Parse.print_table()
