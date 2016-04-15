"""
Convert the HTML file produced by LibreOffice converted from the DOC formatted
file containing the cartoon publications data.

Output: A CSV file with columns delimited by "|".

Note: This script processes one file. For multiple files see html2csv.py.
"""

from bs4 import BeautifulSoup as Bs
import collections
import csv
import os.path

HRMDIR = os.path.join('/', 'Users', 'mlg', 'Documents', 'hrm')
CSVDIR = os.path.join(HRMDIR, 'results')
CSVPATH = os.path.join(CSVDIR, 'final.csv')
HTMLDIR = os.path.join(HRMDIR, 'data')
HTMLPATH = os.path.join(HTMLDIR, 'final.html')


soup = Bs(open(HTMLPATH), 'html.parser')  # , 'html5lib')
outcsv = csv.writer(open(CSVPATH, 'w', newline=''), delimiter='|')

rows = []
table = soup.find('table')
tr = table.find_all('tr')

for row in tr:
    r = [val.text.strip() for val in row.find_all('td')]
    r = [val.replace(u'\xA0', u' ') for val in r]  # nonbreaking space
    if r[0]:
        rows.append(r)

# print(len(rows), rows[2])

irows = iter(rows)
n = 0
for row in irows:
    if n < 10:
        print(row)
    n += 1
    outcsv.writerow(row)
