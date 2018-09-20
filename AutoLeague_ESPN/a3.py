import requests
from bs4 import BeautifulSoup
import pandas as pd
import yaml
import re
from tabulate import tabulate
from AutoLeague_ESPN.parse import Parse

with open('espn_creds.yaml', 'r') as _private:
    privateData = yaml.load(_private)    # pulls in the person specific data (teamId, cookies, etc)

if __name__ == '__main__':
    cookies = {
        'espn_s2': privateData['espn_s2'],
        'SWID': privateData['SWID']
    }

    r = requests.get(privateData['homepage'],
                     cookies=cookies)
    p = Parse()
    # print(r.content)
    p.table_from_source(r.content)
    p.print_table()