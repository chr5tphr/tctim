import sys
from argparse import ArgumentParser

import numpy as np
from PIL import Image

from .core import imprint

def main():
    parser = ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    imprint(np.array(Image.open(args.filename)))

    return 0

if __name__ == '__main__':
    main()
