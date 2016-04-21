"""
Read the CSV file merged from the individual page .doc files by
the tool chain [.doc] --trans2html--> [.html] --html2csv --> [.csv]
and create a dictionary using the Publication, Date, and Page fields as the
key, checking for duplicates.

Read the CSV file created from the corrected doc file and create a similar
dictionary(called "final").

Compare each entry in the merged .csv file with the corresponding entry in the
corrected ("final") .csv file.  Display the mismatches of the 'Title' fields.
There will be many of these as this is what has been corrected. Also check for
any missing records (in either direction).

"""

import collections
import copy
import csv
import os.path
import sys
import time

TRACE_ON = True
RESULTSDIR = os.path.join('/', 'Users', 'mlg', 'Documents', 'hrm', 'results')
CSVDIR = os.path.join(RESULTSDIR, 'csv')
MERGEDPATH = os.path.join(CSVDIR, 'merged.csv')
FINALPATH = os.path.join(CSVDIR, 'cartoons-21apr-datesfixed.csv')
HEADING = ['Title', 'Periodical', 'Date', 'Page', 'File']
"""
The following two files will hold records whose Title field mismatch.
"""


Rowtuple = collections.namedtuple('Rowtuple', ('Seq',) + tuple(HEADING))


def trace(template, *args):
    if TRACE_ON:
        print(template.format(*args))


def opencsvreader(filename):
    csvpath = os.path.join(CSVDIR, filename)
    csvfile = open(csvpath)
    incsv = csv.reader(csvfile, delimiter='|')
    trace('Input: {}', csvpath)
    return incsv


def opencsvwriter(filename):
    csvpath = os.path.join(CSVDIR, filename)
    csvfile = open(csvpath, 'w', newline='')
    outcsv = csv.writer(csvfile, delimiter='|')
    trace('Output: {}', csvpath)
    return outcsv


def build_dict(name, path):
    seq = 0
    reader = opencsvreader(path)
    csvdict = collections.OrderedDict()
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


def compare_dicts(fromgoeff, original):
    corrections = 0
    errors = 0
    corrected = copy.copy(fromgoeff)
    mcorr_writer = opencsvwriter('mergedcorr.csv')
    fcorr_writer = opencsvwriter('finalcorr.csv')
    updated_writer = opencsvwriter('updated.csv')

    for key, row in original.items():
        if key in corrected:
            if row.Title != corrected[key].Title:
                # strip leading row # and trailing filename
                mcorr_writer.writerow(row[1:-1])
                fcorr_writer.writerow(fromgoeff[key][:-1])
                row = list(row)
                row[1] = fromgoeff[key][1]
                corrections += 1
            del corrected[key]
            updated_writer.writerow(row[1:])  # strip off leading row number
        else:
            print('---- original not found:    ', row)
            errors += 1
    print('{} not found in original. {} extras in original:'.format(errors, len(corrected)))
    for key, row in corrected.items():
        print('    extra: ', row)
        errors += 1
    return corrections, errors


def main():
    starttime = time.time()
    merged = build_dict('merged', MERGEDPATH)
    final = build_dict('final', FINALPATH)
    corrections, errors = compare_dicts(final, merged)
    print('End correct_text. Elapsed time: {:.2f} seconds.'.
          format(time.time() - starttime))
    print('{} corrections.'.format(corrections))
    return 1 if errors else 0

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    sys.exit(main())

