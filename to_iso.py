# -*- coding: utf-8 -*-
"""
Convert the dates in the Heath Robinson cartoon transcriptions to ISO 8601
format. This code depends upon knowing what the input file's Date field
contains. If the input file is modified, run the program and for any records
where the ISODate field is "N/A", update the strp_formats tuple as appropriate.
"""

import csv
from datetime import datetime as dt
import os.path
import xlsxwriter


HRMDIR = os.path.join('/', 'Users', 'mlg', 'Documents', 'hrm')
CSVDIR = os.path.join(HRMDIR,  'results')
CSVPATH = os.path.join(CSVDIR, 'merged4.csv')
XLSXDIR = os.path.join(HRMDIR,  'results')
XLSXPATH = os.path.join(XLSXDIR, 'merged4.xlsx')

# Define the date formats that we know will be in the data.
#                1 Jan 18    1 Jan 1918  1.1.18
strp_formats = ('%d %b %y', '%d %b %Y', '%d.%m.%y', '%d/%m/%y', '%d%b %y',
                '%b %y')


def fixdate(rawdate):
    rtn = 'N/A'
    for fmt in strp_formats:
        try:
            fixed = dt.strptime(rawdate, fmt)
            if fixed.year > 1999:
                fixed = dt(fixed.year - 100, fixed.month, fixed.day)
            rtn = fixed.isoformat()[:10]
            break
        except ValueError:
            pass
    return rtn

# Get the original heading from the CSV file and add the column for the ISO
# format date that we will append.
csvfile = open(CSVPATH)
firstline = csvfile.readline()
csvfile.close()
fieldnames = firstline.strip().split('|')
fieldnames += ['ISODate']

# Open the workbook and put the heading line to the worksheet
workbook = xlsxwriter.Workbook(XLSXPATH)
worksheet = workbook.add_worksheet()
colnum = 0
for name in fieldnames:
    worksheet.write(0, colnum, name)
    colnum += 1
# print(CSVPATH)

csvfile = open(CSVPATH, 'r')
reader = csv.DictReader(csvfile, delimiter='|',)
rownum = 1
for row in reader:
        row['ISODate'] = fixdate(row['Date'])
        colnum = 0
        for name in fieldnames:
            worksheet.write(rownum, colnum, row[name])
            colnum += 1
        rownum += 1
workbook.close()
