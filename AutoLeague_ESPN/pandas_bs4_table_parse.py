import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate

def create_team_table(file_name):
    PS = open('..\\offline_webpages\\' + file_name, 'r')
    soup = BeautifulSoup(PS, 'lxml')
    tables = soup.find_all('table')[0]
    df = pd.read_html(str(tables))

    team_table = df[3] # from troubleshooting the third table is the team table
    team_table = team_table.drop([5, 10], axis=1).drop([0, 12], axis=0) # remove useless rows and columns
    team_table = team_table.dropna(subset=[1]) # drop the IR column if PLAYER value is nan

    return team_table

if __name__ == '__main__':
    team_table = create_team_table('front_page_source')

    team_table_str = tabulate(team_table, headers='keys', tablefmt='psql')
    print(team_table_str)
    print(team_table.columns.values)
    print(team_table.index.values)