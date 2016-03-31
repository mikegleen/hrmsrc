"""

"""

from bs4 import BeautifulSoup as bs
import collections
import csv
import os.path

HRMDIR = os.path.join('/', 'Users', 'mlg', 'Documents', 'hrm')
CSVDIR = os.path.join(HRMDIR,  'results')
CSVPATH = os.path.join(CSVDIR, 'merged4.csv')
HTMLDIR = os.path.join(HRMDIR,  'merged')
HTMLPATH = os.path.join(HTMLDIR, 'merged2.html')


soup = bs(open(HTMLPATH), 'html.parser')  # , 'html5lib')
outcsv = csv.writer(open(CSVPATH, 'w', newline=''))

rows = []
table = soup.find('table')
tr = table.find_all('tr')

for row in tr:
    r = [val.text.strip() for val in row.find_all('td')]
    r = [val.replace(u'\xA0', u' ') for val in r]  # nonbreaking space
    rows.append(r)

print(len(rows), rows[2])

irows = iter(rows)
n = 0
for row in irows:
    outcsv.writerow(row)

