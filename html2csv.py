"""
Read each of the HTML files created by trans2html.py, extract the table data,
and create a CSV file with a column appended containing the name of the source
file (minus the trailing .html)
"""

from bs4 import BeautifulSoup as Bs
import collections
import csv
import os.path
import sys

CSVDIR = os.path.join('results', 'csv')
CSVPATH = os.path.join(CSVDIR, 'final.csv')
HTMLDIR = os.path.join('results', 'html')
TRACE_ON = 1


def trace(template, *args):
    if TRACE_ON:
        print(template.format(*args))

# print(len(rows), rows[2])


def handle_one_row(row):
    csvrow = []
    details = row.find_all('td')
    for td in details:
        paras = td.find_all('p')
        detail = ''
        for para in paras:
            # replace whitespace with a single space
            text = ' '.join(para.text.split())
            detail += text + '\n'
        if not detail:  # if there was no <p> tag
            detail = td.text
        detail = detail.strip()  # remove trailing NL
        csvrow.append(detail)
    return csvrow


def handle_one_file(outcsv, htmlpath, name):
    filepath = os.path.join(htmlpath, name)
    trace('        filepath: {}', filepath)
    htmlfile = open(filepath)
    soup = Bs(htmlfile, 'html.parser')  # , 'html5lib')
    table = soup.find('table')
    rows = table.find_all('tr')

    for row in rows:
        outrow = handle_one_row(row)
        # ignore empty rows and title rows
        if len(outrow) > 3 and outrow[0] and outrow[1] != 'Periodical':
            outrow.append(name[:-5])  # all but trailing ".html"
            outcsv.writerow(outrow)
    htmlfile.close()


def handle_subdir(outcsv, dirname):
    # handle transcribexxx directory under results/html
    html_sub_path = os.path.join(HTMLDIR, dirname)
    trace('{}', html_sub_path)
    for name in os.listdir(html_sub_path):
        trace('    {}', name)
        if name.lower().endswith('.html'):
            handle_one_file(outcsv, html_sub_path, name)
        else:
            trace('        skipping {}', name)


def main():
    outcsv = csv.writer(open(CSVPATH, 'w', newline=''), delimiter='|')
    for name in os.listdir(HTMLDIR):
        if os.path.isdir(os.path.join(HTMLDIR, name)):
            handle_subdir(outcsv, name)


def one_file():
    csvname = sys.argv[1][:-5] + '.csv'
    csvfile = open(os.path.join(CSVDIR, csvname), 'w', newline='')
    outcsv = csv.writer(csvfile, delimiter='|')
    handle_one_file(outcsv, HTMLDIR, sys.argv[1])


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    if len(sys.argv) < 1:
        main()
    else:
        one_file()
