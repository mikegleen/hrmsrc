#!/usr/bin/python
"""
Convert a PDF file to JPEG using the OSX utility sips.

The files must reside in directories with predefined names all within a
predefined base directory (see below).

To use this script, copy your PDF file to the "pdf" subdirectory of the base
directory.

The script will create a JPEG file in the "jpg" subdirectory and move the PDF
file to the "archive" subdirectory.

"""

from __future__ import print_function
import os.path
import re
import shutil
import subprocess

BASEDIR = '/users/mlg/play/hrm'
SIPSCMD = 'sips -s format jpeg "{pdf_file}" --out "{jpg_file}"'
VERBOS = 0

if __name__ == '__main__':
    pdfbase = os.path.join(BASEDIR, 'pdf')
    jpgbase = os.path.join(BASEDIR, 'jpg')
    archivebase = os.path.join(BASEDIR, 'archive')
    for pdfname in os.listdir(pdfbase):
        pdfpath = os.path.join(pdfbase, pdfname)
        if VERBOS > 0:
            print(pdfpath)
        if os.path.isdir(pdfpath):
            continue
        leadpart, extension = os.path.splitext(pdfname)
        if extension.lower() != '.pdf':
            continue
        jpegname = leadpart + '.jpg'
        jpegpath = os.path.join(jpgbase, jpegname)
        if VERBOS > 0:
            print (jpegpath)
        scmd = SIPSCMD.format(pdf_file=pdfpath, jpg_file=jpegpath)
        if VERBOS > 0:
            print(scmd)
        subprocess.check_call(scmd, shell=True)
        shutil.move(pdfpath, archivebase)
