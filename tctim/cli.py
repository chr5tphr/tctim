import sys
from imageio import imread
from argparse import ArgumentParser

from .core import imprint

def main():
    parser = ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    if args.filename == '-':
        raw = sys.stdin.buffer.read()
    else:
        raw = args.filename

    im = imread(raw)
    imprint(im)

    return 0

if __name__ == '__main__':
    main()
