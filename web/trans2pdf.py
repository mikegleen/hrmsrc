# -*- coding: utf-8 -*-  needed because of embedded "£"
"""
Convert all of the .doc or .docx format files in a directory to pdf.

Requires libreOffice to be installed and a batch file created containing:
    /Applications/LibreOffice.app/Contents/MacOS/soffice "$@"

WARNING: if soffice exits without printing anything, check that you don't have
         libreOffice running in the background.
"""

import os
import os.path
import subprocess
import sys
import time

CMD = ('/Users/mlg/bin/soffice;--headless;--convert-to;pdf;{docfile};'
       '--outdir;{pdfdir}')
DOCDIR = os.path.join('data', 'doc')
PDFDIR = os.path.join('results', 'pdf')


def main():
    starttime = time.time()
    for name in os.listdir(DOCDIR):
        base, ext = os.path.splitext(name)
        if ext.lower() in ('.doc', '.docx'):
            docfile = os.path.join(DOCDIR, name)
            pdf_file = name[:-len(ext)] + '.pdf'
            pdf_file = os.path.join(PDFDIR, pdf_file)
            if os.path.exists(pdf_file) and (os.path.getmtime(docfile) <
                                             os.path.getmtime(pdf_file)):
                print('        unmodified: ', name)
                continue
            cmd = CMD.format(docfile=docfile, pdfdir=PDFDIR)
            print('        ', cmd)
            subprocess.check_call(cmd.split(';'))
        else:
            print('        skipping ', name)
    print('End trans2pdf. Elapsed time: {:.2f} seconds.'.format(
        time.time() - starttime))
    return 0


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    sys.exit(main())

