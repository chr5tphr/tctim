from sys import stdout
from os import get_terminal_size
from logging import getLogger

import numpy as np
from PIL import Image


logger = getLogger(__name__)


def _tctim(array):
    if (
        not isinstance(array, np.ndarray) or
        (array.dtype != np.uint8) or
        (len(array.shape) != 3) or
        (array.shape[2] != 3) or
        (array.shape[0] % 2)
    ):
        raise TypeError('Input has to be a numpy array with dtype uint8, 3 axes, 3 channels in the last axis and an even number of rows!')
    COL_FMT = '\x1b[48;2;%d;%d;%dm\x1b[38;2;%d;%d;%dm'
    COL_CLR = '\x1b[0m'
    rows = [
        ''.join([
            COL_FMT%tuple(top.tolist() + bot.tolist()) + '▄' for top, bot in zip(*drow)
        ]) for drow in zip(array[0::2], array[1::2])
    ]
    imstr = ((COL_CLR + '\n').join(rows)) + COL_CLR
    return imstr


def _fit_term(image, fbacksize=(64, 64)):
    try:
        tsize = get_terminal_size()
        nrow, ncol = 2 * tsize.lines, tsize.columns
    except OSError:
        ncol, nrow = fbacksize

    image = image.copy()
    image.thumbnail((ncol, nrow))
    return image


def _imgify(obj, bbox=None, fit_term=True):
    try:
        array = np.array(obj)
    except TypeError as err:
        raise TypeError('Could not cast instance of \'{}\' to numpy array.'.format(str(type(obj)))) from err

    if len(array.shape) not in (2, 3):
        raise TypeError('Input has to have either 2 or 3 axes!')

    if (len(array.shape) == 3) and (array.shape[2] not in (1, 3, 4)):
        raise TypeError('Last axis of input are color channels, which have to either be 1, 3, 4 or be omitted entirely!')

    # rescale data if necessary
    if array.dtype != np.uint8:
        if bbox is None:
            lo, hi = array.min(), array.max()
        else:
            lo, hi = bbox
        array = ((array - lo) * 255/(hi-lo)).clip(0, 255).astype(np.uint8)

    # add missing axis if omitted
    if len(array.shape) == 2:
        array = array[:,:,None]

    # resolve alpha channel
    if array.shape[2] == 4:
        array = (array[:,:,:3].astype(np.float32) * array[:,:,3:].astype(np.float32) / 255.).clip(0., 255.).astype(np.uint8)

    # grayscale to rgb
    if array.shape[2] == 1:
        array = np.repeat(array, 3, axis=2)

    # fit to terminal
    if fit_term:
        array = np.array(_fit_term(Image.fromarray(array)))

    # pad a final line if number of rows is odd
    if array.shape[0] % 2:
        array = np.concatenate([array, np.zeros((1, array.shape[1], 3), dtype=np.uint8)], axis=0)

    return array


def tctim(array, montage=False, bbox=None, fit_term=True):
    if montage:
        array = _montage(array)
    array = _imgify(array, bbox=bbox, fit_term=fit_term)
    return _tctim(array)


def imprint(array, montage=False, bbox=None, fit_term=True, file=stdout, flush=False):
    print(tctim(array, montage=montage, bbox=bbox, fit_term=fit_term), file=file, flush=flush)


def _montage(array, shape=None, fallback=(64, 64)):
    if not isinstance(array, np.ndarray):
        raise TypeError('Only numpy arrays are supported!')
    if len(array.shape) not in (3, 4):
        raise TypeError('For a montage the array has to have either 3 (grayscale) or 4 (rgb) axes!')

    # add missing axis if omitted
    if len(array.shape) == 3:
        array = array[(slice(None),) * 3 + (None,)]

    if shape is None:
        try:
            tsize = get_terminal_size()
            nrow, ncol = 2 * tsize.lines, tsize.columns
        except OSError:
            ncol, nrow = fallback

        N, H, W, C = array.shape
        w = ncol // W
        h = (N + w - 1) // w
    else:
        h, w = shape

    ret = np.ones((h * w, H, W, C), dtype=array.dtype) * array.min()
    dim = min(N, h * w)
    ret[:dim] = array[:dim]
    ret = ret.reshape(h, w, H, W, C).transpose(0, 2, 1, 3, 4).reshape(h * H, w * W, C)

    return ret
