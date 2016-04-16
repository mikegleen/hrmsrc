"""
Read the CSV file created by html2csv, and create a dictionary using the
Publication, Date, and Page fields as the key, checking for duplicates.
"""

import collections
import csv
import os.path
import sys

TRACE_ON = True
HRMDIR = os.path.join('/', 'Users', 'mlg', 'Documents', 'hrm')
CSVDIR = os.path.join(HRMDIR, 'results', 'csv')
MERGEDPATH = os.path.join(CSVDIR, 'merged.csv')
FINALPATH = os.path.join(CSVDIR, 'final.csv')
FIXEDPATH = os.path.join(CSVDIR, 'fixed.csv')
HEADING = ['Title', 'Periodical', 'Date', 'Page', 'File']
Rowtuple = collections.namedtuple('Rowtuple', ('Seq',) + tuple(HEADING))


def trace(template, *args):
    if TRACE_ON:
        print(template.format(*args))


def opencsvreader(filename):
    global csvpath
    csvpath = os.path.join(CSVDIR, filename)
    csvfile = open(csvpath)
    incsv = csv.reader(csvfile, delimiter='|')
    trace('Input: {}', csvpath)
    return incsv


def opencsvwriter(filename):
    global csvpath
    csvpath = os.path.join(CSVDIR, filename)
    csvfile = open(csvpath, 'w', newline='')
    outcsv = csv.writer(csvfile, delimiter='|')
    outcsv.writerow(HEADING)
    trace('Output: {}', csvpath)
    return outcsv


def build_dict(name, path):
    seq = 0
    reader = opencsvreader(path)
    csvdict = {}
    for row in reader:
        seq += 1
        nrow = Rowtuple(seq, *row)
        key = (nrow.Periodical, nrow.Date, nrow.Page)
        if key in csvdict:
            old = csvdict[key]
            print('------------\nDuplicate: {} seq {}, {}'.
                  format(name, old.Seq, seq))
            print(old)
            print('----')
            print(nrow)
        else:
            csvdict[key] = nrow
    trace('Merged: {} rows processed. Dict len: {}', seq, len(csvdict))
    return csvdict


def build_merged_dict():
    seq = 0
    mergedcsv = opencsvreader(MERGEDPATH)
    merged = {}
    for row in mergedcsv:
        seq += 1
        nrow = Rowtuple(seq, *row)
        key = (nrow.Periodical, nrow.Date, nrow.Page)
        if key in merged:
            old = merged[key]
            print('------------\nDuplicate: seq {}, {}'.format(old.Seq, seq))
            print(old)
            print('----')
            print(nrow)
        else:
            merged[key] = nrow
    trace('Merged: {} rows processed. Dict len: {}', seq, len(merged))
    return merged


def main():
    merged_dict = build_dict('merged', MERGEDPATH)
if __name__ == '__main__':
    rowcount = 0
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    main()

