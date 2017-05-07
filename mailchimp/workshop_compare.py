# -*- coding: utf-8 -*-  needed because of embedded "£"
"""

"""
import csv
import os
import pandas.io.excel as ex
import sys


def prune(wdict, mcfilename):
    """
    
    :param wdict: dictionary of email addresses from the workshop excel file   
    :param mcfilename: a MailChimp CSV file containing email addresses that
            we must delete from wdir
    :return: None
    """
    # Extract preamble from the filename. For example:
    # subscribed_members_export_00d72831eb.csv -> subscribed
    preamble = mcfilename.split('_')[0]
    notdups, dups = 0, 0
    with open(mcfilename, newline='') as csvfile:
        chimpreader = csv.reader(csvfile)
        next(chimpreader)
        for row in chimpreader:
            email = row[0]
            if email in wdict:
                dups += 1
                del wdict[email]
                print('  del:', email, ',', preamble)
    print(preamble, 'dups found:', dups)


def main(workshop, mailchimpdir):
    wdict = {}
    wdf = ex.read_excel(workshop, 'Sheet1', parse_cols=(0, 1, 2))
    wdf.rename(columns={'Surname': 'surname',
                        'First name': 'first_name',
                        'Email address': 'email_address'},
               inplace=True)
    for row in wdf.itertuples():
        # print(row)
        wdict[row.email_address] = row
    for filename in os.listdir(mailchimpdir):
        if not filename.endswith('.csv'):
            continue
        prune(wdf, filename)


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        print('Two parameters needed, the workshop XLSX file and the'
              ' mailchimp CSV directory.')
