# -*- coding: utf-8 -*-  needed because of embedded "£"
"""
Create two thumbnail images:
    portrait: width 342, height 484
    landscape: width 1280, height 826

The background color is hard-coded below.

"""
import argparse
import math
import os.path
from PIL import Image
import sys

BACKGROUND = (0xF2, 0xF4, 0xF6)
PORTRAIT_WIDTH = 342
PORTRAIT_HEIGHT = 484
PORTRAIT_RATIO = float(PORTRAIT_WIDTH) / float(PORTRAIT_HEIGHT)
LANDSCAPE_WIDTH = 1280
LANDSCAPE_HEIGHT = 826
LANDSCAPE_RATIO = float(LANDSCAPE_WIDTH) / float(LANDSCAPE_HEIGHT)


def pad_height(inimage, target_width, target_height):
    """
    The input image is too wide. Resize it so that the width is target_width
    and then pad the top and bottom so that the height is target_height.

    :param inimage:
    :param target_width:
    :param target_height:
    :return the resized and padded image
    """
    width, height = inimage.size
    hw_ratio = float(height) / float(width)
    unpadded_height = int(target_height * hw_ratio)
    resized_image = inimage.resize((target_width, unpadded_height))
    y_origin = int(math.ceil((target_height - unpadded_height) / 2.))
    target_image = Image.new('RGBA', (target_width, target_height),
                             BACKGROUND)
    target_image.paste(resized_image, (0, y_origin))
    return target_image


def pad_width(inimage, target_width, target_height):
    """
    The input image is too tall. Resize it so that the height is target_height
    and then pad the left and right so that the width is target_width.

    :param inimage:
    :param target_width:
    :param target_height:
    :return the resized and padded image
    """
    width, height = inimage.size
    wh_ratio = float(width) / float(height)
    unpadded_width = int(target_width * wh_ratio)
    resized_image = inimage.resize((unpadded_width, target_height))
    x_origin = int(math.ceil((target_width - unpadded_width) / 2.))
    target_image = Image.new('RGBA', (target_width, target_height),
                             BACKGROUND)
    target_image.paste(resized_image, (x_origin, 0))
    return target_image


def main(args):
    basename = os.path.basename(args.infile)  # 'a/b/xyz.jpg' -> 'xyz.jpg'
    front, extension = os.path.splitext(basename)  # 'xyz.jpg' -> 'xyz', '.jpg'
    portrait_thumb_name = front + '_portrait_thumb' + '.jpeg'
    landscape_thumb_name = front + '_landscape_thumb' + '.jpeg'
    portrait_target = os.path.join(args.outdir, portrait_thumb_name)
    landscape_target = os.path.join(args.outdir, landscape_thumb_name)
    input_image = Image.open(args.infile)
    width, height = input_image.size
    if width / height > PORTRAIT_RATIO:
        portrait = pad_height(input_image)
    else:
        portrait = pad_width(input_image)
    if width / height > LANDSCAPE_RATIO:
        landscape = pad_height(input_image)
    else:
        landscape = pad_width(input_image)


def get_args():
    parser = argparse.ArgumentParser(description='''
    Create a montage of a portrait format image and a plain landscape
    background so that it won't be cropped by the LiberateIT CMS. The height
    is multiplied by √2 and the bias to give the new width.
    ''')
    parser.add_argument('infile', help='''Landscape format input file.''')
    parser.add_argument('-b', '--bias', help='''
        The bias is an arbitrary multiplier to give a large enough width to
        avoid cropping. The default value is 1.25.
        ''', type=float, default=1.25)
    parser.add_argument('-o', '--outdir', help='''Directory to contain the
        output landscape file. If omitted, the default is "results/landscape".
        ''', default=os.path.join('results', 'thumb'))
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    _args = get_args()
    main(_args)
