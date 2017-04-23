# -*- coding: utf-8 -*-  needed because of embedded "£"
"""

"""
import csv
import pandas as pd
import pandas.io.excel as ex
import sys


def main(workshop, mailchimp):
    wdict = {}
    wdf = ex.read_excel(workshop, 'Sheet1', parse_cols=(0, 1, 2))
    wdf.rename(columns={'Surname': 'surname',
                        'First name': 'first_name',
                        'Email address': 'email_address'},
               inplace=True)
    for row in wdf.itertuples():
        # print(row)
        wdict[row.email_address] = row
    notdups, dups = 0, 0
    with open(mailchimp, newline='') as csvfile:
        chimpreader = csv.reader(csvfile)
        next(chimpreader)
        for row in chimpreader:
            email = row[0]
            if email in wdict:
                dups += 1
                print('dup found: ', email)
            else:
                notdups += 1
                print('******not dup:', email)
    print('dups {}'.format(dups))
    print('notdups {}'.format(notdups))
    print(len(wdf))

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        print('Two parameters needed, the workshop XLSX file and the'
              ' mailchimp CSV file.')
