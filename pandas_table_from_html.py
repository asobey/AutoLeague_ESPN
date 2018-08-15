#!python3
#From Website: https://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/

import pandas as pd
from bs4 import BeautifulSoup

html_string = '''
      <table>
            <tr>
                <td> Hello! </td>
                <td> Table </td>
            </tr>
        </table>
    '''

#soup = BeautifulSoup(html_string, 'lxml')  # Parse the HTML as a string
PS = open('front_page_source', 'r')
soup = BeautifulSoup(PS, 'lxml')

table = soup.find_all('table')[0]  # Grab the first table

new_table = pd.DataFrame(columns=range(0, 11), index=[10])  # I know the size, need to find size

row_marker = 0
for row in table.find_all('tr'):
    column_marker = 0
    columns = row.find_all('td')
    for column in columns:
        new_table.iat[row_marker, column_marker] = column.get_text()
        column_marker += 1

print(new_table)
