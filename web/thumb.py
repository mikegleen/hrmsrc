# -*- coding: utf-8 -*-  needed because of embedded "£"
"""
Create thumbnail images.

See get_args for details.

"""
import argparse
from collections import namedtuple
import math
import os.path
from PIL import Image
import sys

BACKGROUND = 'F2F4F6'

Img = namedtuple('Img', ['w', 'h', 'name', 'background'])

THUMB_IMG_SIZES = {
    'ev-p': Img(342, 484, 'event portrait', 'FFFFFF'),
    'ev-l': Img(1280, 826, 'event landscape', 'FFFFFF'),
    'm-t': Img(1280, 826, 'media centre thumbnail', 'FFFFFF'),
    'n-t': Img(1280, 826, 'news thumbnail', 'FFFFFF'),
    'n-w': Img(1280, 410, 'news wide', 'FFFFFF'),
    'ex-t': Img(700, 454, 'exhibition thumbnail', BACKGROUND),
}


def trace(level, template, *args):
    if _args.verbose >= level:
        print(template.format(*args))


def make_background_tuple(hexstr):  # hexstr can be like F1F2F3 or 0xF1F2F3
    hexint = int(hexstr, 16)
    red = (hexint >> 16) & 0xFF
    green = (hexint >> 8) & 0xFF
    blue = hexint & 0xFF
    return red, green, blue


def pad_height(inimage, target_width, target_height, background):
    """
    The input image is too wide. Resize it so that the width is target_width
    and then pad the top and bottom so that the height is target_height.

    :param inimage:
    :param target_width:
    :param target_height:
    :param background: 3-tuple of red, blue, green
    :return the resized and padded image
    """
    trace(2, 'Begin pad_height. Target width, height = ({}, {})', target_width,
          target_height)
    width, height = inimage.size
    wh_ratio = float(width) / float(height)
    unpadded_height = int(round(target_width / wh_ratio))
    trace(2, 'Resizing image to ({}, {})', target_width, unpadded_height)
    resized_image = inimage.resize((target_width, unpadded_height))
    y_origin = int(math.ceil((target_height - unpadded_height) / 2.))
    target_image = Image.new('RGBA', (target_width, target_height),
                             background)
    target_image.paste(resized_image, (0, y_origin))
    return target_image


def pad_width(inimage, target_width, target_height, background):
    """
    The input image is too tall. Resize it so that the height is target_height
    and then pad the left and right so that the width is target_width.

    :param inimage:
    :param target_width:
    :param target_height:
    :param background:
    :return the resized and padded image
    """
    trace(2, 'Begin pad_width. Target width, height = ({}, {})', target_width,
          target_height)
    width, height = inimage.size
    wh_ratio = float(width) / float(height)
    unpadded_width = int(round(target_height * wh_ratio))
    trace(2, "Resizing image to ({}, {})", unpadded_width, target_height)
    resized_image = inimage.resize((unpadded_width, target_height))
    x_origin = int(math.ceil((target_width - unpadded_width) / 2.))
    target_image = Image.new('RGBA', (target_width, target_height),
                             background)
    target_image.paste(resized_image, (x_origin, 0))
    return target_image


def onefile(infile, outdir, img_sizes):
    """
    Iterate over the target image sizes that we want to create and resize and
    pad them accordingly.
    """
    basename = os.path.basename(infile)  # 'a/b/xyz.jpg' -> 'xyz.jpg'
    front, extension = os.path.splitext(basename)  # 'xyz.jpg' -> 'xyz', '.jpg'
    try:
        input_image = Image.open(infile)
    except OSError:
        print('Skipping unrecognized file:', infile)
        return
    width, height = input_image.size
    wh_ratio = width / height
    trace(2, "Input: {}\nSize (width, height) in pixels: {}, {}, "
          "width/height = {:.3f}", infile, width, height, wh_ratio)
    for key in img_sizes:
        thumb_width, thumb_height, thumb_name, background = img_sizes[key]
        if _args.background:
            background = _args.background
        # 'FFFFFF' -> (255,255,255)
        background_tuple = make_background_tuple(background)
        trace(2, 'Background color: (0x{:02X}, 0x{:02X}, 0x{:02X})',
              background_tuple)
        thumb_wh_ratio = float(thumb_width) / float(thumb_height)
        if wh_ratio > thumb_wh_ratio:
            thumb_image = pad_height(input_image, thumb_width, thumb_height,
                                     background_tuple)
        else:
            thumb_image = pad_width(input_image, thumb_width, thumb_height,
                                    background_tuple)
        thumb_file_name = front + '_thumb_' + key + extension
        thumb_path = os.path.join(outdir, thumb_file_name)
        trace(1, 'Saving thumbnail: {}, ({})', thumb_path, thumb_name)
        thumb_image.save(thumb_path)


def main(args):
    os.makedirs(args.outdir, exist_ok=True)
    wh = THUMB_IMG_SIZES
    background = _args.background if _args.background else BACKGROUND
    if args.width:
        wh = {'th': (args.width, args.height, 'anonymous', background)}
    elif args.key:
        img = THUMB_IMG_SIZES[args.key]
        wh = {args.key: img}
    if os.path.isdir(args.infile):
        for filename in os.listdir(args.infile):
            if '_thumb_' in filename:
                continue
            onefile(filename, args.outdir, wh)
    else:
        onefile(args.infile, args.outdir, wh)


def get_args():
    q = THUMB_IMG_SIZES
    thumblist = ('\n    key   W x H     Description' +
                 ''.join(['\n    {:5} {:9} {}'
                         .format(x,
                                 '{}x{}'.format(q[x].w, q[x].h),
                                 q[x].name) for x in q]))
    parser = argparse.ArgumentParser(formatter_class=
                                     argparse.RawDescriptionHelpFormatter,
                                     description='''
    Create multiple thumbnail images using a predefined set of dimensions or
    width and height values passed as parameters.

    The thumbnail files are created with the same name as the original file
    but with the designated abbreviation appended before the extension. Thus
    "jellytots.jpeg" becomes "jellytots_thumb_ev-l.jpeg" for Event Landscape
    thumbnail files. The default thumbnail files produced are:
    ''' + thumblist)
    parser.add_argument('infile', help='''There are two modes. If infile is
    a simple file, it is processed and output files are written to outdir.
    If it is a directory, all of the files in that directory are processed and
    output is written to the same directory. To prevent output files being
    re-processed, file names including "_thumb_" are skipped.''')
    parser.add_argument('-b', '--background', help='''
        Hex number describing the background color. The default depends upon
        which thumbnail is being produced.
        The number should be coded as six hex digits. The leading "0x" is
        optional. If the number given is not valid hexadecimal, the program
        will abort.''')
    parser.add_argument('--height', type=int, default=0, help='''
        Set an explicit height to pad to (sorry, -h is taken). You must also
        specify width. If specified, a single thumbnail file is created rather
        than the set of files internally defined. An abbreviation of 'th' is
        used for the output filename.
        ''')
    parser.add_argument('-k', '--key', help='''Specifies a single thumbnail
    to produce. Do not specify a key and also an explicit width and height.
    ''')
    parser.add_argument('-o', '--outdir', help='''Directory to contain the
        output landscape file. If omitted, the default is the directory
        "thumb" in the same directory that the input file resides.
        ''')
    parser.add_argument('-v', '--verbose', type=int, default=1, help='''
        Set the verbosity. The default is 1 which prints summary information.
        ''')
    parser.add_argument('-w', '--width', type=int, default=0, help='''
        Set an explicit width to pad to. You must also specify height.
        ''')

    args = parser.parse_args()
    if bool(args.height) != bool(args.width):
        raise ValueError('You must specify either both width and height or'
        + ' neither.')
    if bool(args.key) and bool(args.height):
        raise ValueError('You may not specify both the key and also height'
                         + ' and width.')
    if args.key and args.key not in THUMB_IMG_SIZES:
        raise ValueError('Unrecognized key.')
    if not args.outdir:
        if os.path.isdir(args.infile):
            args.outdir = args.infile
        else:
            args.outdir, _ = os.path.split(args.infile)
        args.outdir = os.path.join(args.outdir, 'thumb')
    return args

if __name__ == '__main__':

    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    try:
        _args = get_args()
    except ValueError as v:
        print(v)
        sys.exit(1)
    main(_args)
