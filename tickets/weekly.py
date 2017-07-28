# -*- coding: utf-8 -*-
"""
Produce a report of the weekly revenue.
Input is the file produced by clean.py.
"""

import argparse
import datetime
import os.path
import pandas as pd
import sys

from admission_types import ADMISSION_TYPES


OUTDIR = '/Users/mlg/pyprj/hrm/results/analytics/tickets'

# df[df['A'].isin([3, 6])]


def one_report(df, suffix):
    outreport = os.path.join(_args.outdir, _basename + '_weekly_' + suffix
                             + '.xlsx')
    g = df.groupby(['date', 'type'])
    gg = g.sum().unstack().fillna('')
    gg['weektot'] = df.groupby('date').sum()['totprice']

    gg.to_excel(outreport)


def main():
    incsvfile = _args.infile
    df = pd.read_csv(incsvfile,
                     names='date quantity type totprice'.split(),
                     usecols=(0,1,2,4),
                     index_col=False)
    dfdate = pd.to_datetime(df.date, format='%d/%m/%Y')
    # Coerce the date to be the first day of the week (Monday).
    df['date'] = dfdate - pd.to_timedelta(dfdate.dt.dayofweek, unit='D')
    if _args.month:
        m = df.date.dt.month
        y = df.date.dt.year
        df = df[(m == _args.month) & (y == _args.year)]
    one_report(df, 'full')
    df2 = df[df.type.isin(ADMISSION_TYPES)]
    one_report(df2, 'admission')
    df3 = df[~df.type.isin(ADMISSION_TYPES)]
    one_report(df3, 'other')


def getargs():
    parser = argparse.ArgumentParser(
        description='''
        Produce a report of the weekly revenue.
        Input is the file produced by clean.py.
        Three reports are produced. The "full" report contains all types of
        ticket sales. The "admission" report contains only the types marked as
        admission sales in the configuration file 'admission_types.py". The
        "other" report contains non-admission sales.
        ''')
    parser.add_argument('infile', help='''
         The CSV file that has been cleaned by tickets.clean.py''')
    parser.add_argument('-m', '--month', type=int,
                        choices=list(range(1, 13)), help='''
    If specified, limit reporting to the given month in the current year.''')
    parser.add_argument('-o', '--outdir', help='''Directory to contain the
        output report file. If omitted, the default is the directory
        "results" in the same directory that the input file resides.
        ''')
    args = parser.parse_args()
    if not args.outdir:
        args.outdir = OUTDIR
    return args


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    _args = getargs()
    _basename = os.path.split(_args.infile)[1]
    _basename = os.path.splitext(_basename)[0]
    main()
