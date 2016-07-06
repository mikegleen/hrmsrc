# -*- coding: utf-8 -*-  needed because of embedded "£"
"""

"""

from pyPDF2 import PdfFileWriter, PdfFileReader
import sys


def main():
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open("document-page{}.pdf".format(i), "wb") as outputStream:
            output.write(outputStream)

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    inputpdf = PdfFileReader(open("document.pdf", "rb"))
    main()
