# -*- coding: utf-8 -*-  needed because of embedded "£"
"""
Input is a PDF file specified in the first parameter.
Output is one file in the current directory per page in the input file. The
name of the output files is <input basename>-page<n> starting with the zero-th
page.
"""
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import sys


def main(infilename):
    inputpdf = PdfFileReader(open(infilename, "rb"))
    basename = os.path.splitext(infilename)[0]
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open("{}-page{}.pdf".format(basename, i), "wb") as outputStream:
            output.write(outputStream)

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    main(sys.argv[1])
