# -*- coding: utf-8 -*-  needed because of embedded "£"
"""
Create a montage of a portrait format image and a plain landscape background
so that it won't be cropped by the LiberateIT CMS.

The background color is hard-coded below.

"""
import argparse
import math
import os.path
from PIL import Image
import sys

BACKGROUND = (0xF2, 0xF4, 0xF6)


def main(args):
    basename = os.path.basename(args.infile)  # 'a/b/xyz.jpg' -> 'xyz.jpg'
    front, extension = os.path.splitext(basename)  # 'xyz.jpg' -> 'xyz', '.jpg'
    landscape_name = front + '_landscape' + extension
    target = os.path.join(args.outdir, landscape_name)
    portrait_image = Image.open(args.infile)
    width, height = portrait_image.size

    new_width = int(height * 2.**.5 * args.bias)
    if new_width <= width:
        print('Image is already wide enough.')
        portrait_image.save(target)
        sys.exit(0)

    x_origin = int(math.ceil((new_width - width) / 2.))
    landscape_image = Image.new('RGBA', (new_width, height), BACKGROUND)
    landscape_image.paste(portrait_image, (x_origin, 0))
    landscape_image.save(target)


def get_args():
    parser = argparse.ArgumentParser(description='''
    Create a montage of a portrait format image and a plain landscape
    background so that it won't be cropped by the LiberateIT CMS. The height
    is multiplied by √2 and the bias to give the new width.
    ''')
    parser.add_argument('infile', help='''Portrait format input file.''')
    parser.add_argument('-b', '--bias', help='''
        The bias is an arbitrary multiplier to give a large enough width to
        avoid cropping. The default value is 1.25.
        ''', type=float, default=1.25)
    parser.add_argument('-o', '--outdir', help='''Directory to contain the
        output landscape file. If omitted, the default is "results/landscape".
        ''', default=os.path.join('results', 'landscape'))
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    _args = get_args()
    main(_args)
