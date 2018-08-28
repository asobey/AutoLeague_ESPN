import pandas as pd
from tabulate import tabulate
import pandas_bs4_table_parse

team_table = pandas_bs4_table_parse.create_team_table('front_page_source')

team_table_str = tabulate(team_table, headers='keys', tablefmt='psql')
print(team_table_str)
print(team_table.columns.values)
print(team_table.index.values)

positions = ['QB', 'TE', 'K', 'D/ST', 'RB', 'WR']

for pos in positions:
    #print(team_table)
    print(pos)
    # This could be a problem: ValueError: cannot index with vector containing NA / NaN values
    # Try Except will not work. Maybe remove index if not filled
    print(team_table.index[team_table[1].str.contains(pos)].values)