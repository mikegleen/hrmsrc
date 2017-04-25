# -*- coding: utf-8 -*-
"""
Produce a report of the daily revenue.
Input is the file produced by clean.py.
"""

import pandas as pd
import sys


def main(incsvfile, outreport):
    df = pd.read_csv(incsvfile,
                     usecols=(0, 1, 2, 4),
                     names='date quantity type totprice'.split(),
                     index_col=False)
    df.date = pd.to_datetime(df.date, format='%d/%m/%Y')
    g = df.groupby(['date', 'type'])
    gg = g.sum().unstack().fillna('')
    gg['datetot'] = df.groupby('date').sum()['totprice']
    gg.to_excel(outreport)


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    if len(sys.argv) > 2:
        inf = sys.argv[1]
        outf = sys.argv[2]
        main(inf, outf)
    else:
        print('Two parameters needed, the input cleaned file and the'
              ' output report file.')
