# -*- coding: utf-8 -*-
"""
Produce a report of the weekly revenue.
Input is the file produced by clean.py.
"""

import pandas as pd
import sys


def main(incsvfile, outreport):
    df = pd.read_csv(incsvfile,
                     names='date quantity type totprice'.split(),
                     usecols=(0,1,2,4),
                     index_col=False)
    dfdate = pd.to_datetime(df.date, format='%d/%m/%Y')
    df['date'] = dfdate - pd.to_timedelta(dfdate.dt.dayofweek, unit='D')
    g = df.groupby(['date', 'type'])
    gg = g.sum().unstack().fillna('')
    gg['weektot'] = df.groupby('date').sum()['totprice']
    gg.to_excel(outreport)


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    if len(sys.argv) > 2:
        inf = sys.argv[1]
        outf = sys.argv[2]
        main(inf, outf)
    else:
        print('Two parameters needed, the output of clean.py and the'
              ' output report file.')
