# -*- coding: utf-8 -*-
"""
    Clean the Ticket Report file.
    1. Delete the first 4 lines of title, comments, etc.
    2. Convert the input latin-1 (iso-8859-1) input to utf-8
    3. Delete lines starting with ' ' which are summary lines.
"""
import codecs
import sys


def main(infile, outfile):
    for i in range(4):
        next(infile)
    for line in infile:
        if line[0] != ' ':
            outfile.write(line)

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    if len(sys.argv) > 2:
        inf = sys.argv[1]
        outf = sys.argv[2]
        with codecs.open(inf, 'r', 'latin_1') as incsv,\
                open(outf, 'w') as outcsv:
            main(incsv, outcsv)
    else:
        print('Two parameters needed, the original ticket report and the'
              ' output cleaned file.')
