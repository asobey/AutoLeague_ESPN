import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate

PS = open('front_page_source', 'r')
soup = BeautifulSoup(PS,'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))

#print(df)
print( tabulate(df[3], headers='keys', tablefmt='psql') )