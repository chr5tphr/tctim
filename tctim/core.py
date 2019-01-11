import numpy as np

from sys import stdout
from os import get_terminal_size
from logging import getLogger
from PIL.Image import open as imopen

logger = getLogger(__name__)


def _tctim(im):
    if not isinstance(im, np.ndarray) or (im.dtype != np.uint8) or (len(im.shape) != 3) or (im.shape[2] != 3) or (im.shape[0] % 2):
        raise TypeError('Input has to be a numpy array with dtype uint8, 3 axes, 3 channels in the last axis and an even number of rows!')
    COL_FMT = '\x1b[48;2;%d;%d;%dm\x1b[38;2;%d;%d;%dm'
    COL_CLR = '\x1b[0m'
    rows = [''.join([COL_FMT%tuple(top.tolist() + bot.tolist()) + '▄' for top, bot in zip(*drow)]) for drow in zip(im[0::2], im[1::2])]
    imstr = ((COL_CLR + '\n').join(rows)) + COL_CLR
    return imstr

def _imgify(im, bbox=None):
    if not isinstance(im, np.ndarray):
        raise TypeError('Only numpy arrays are supported!')
    if len(im.shape) not in [2, 3]:
        raise TypeError('Input has to have either 2 or 3 axes!')
    if (len(im.shape) == 3) and (im.shape[2] not in [1, 3, 4]):
        raise TypeError('Last axis of input are color channels, which have to either be 1, 3, 4 or be omitted entirely!')

    # rescale data if necessary
    if im.dtype != np.uint8:
        if bbox is None:
            lo, hi = im.min(), im.max()
        else:
            lo, hi = bbox
        im = ((im - lo) * 255/(hi-lo)).clip(0, 255).astype(np.uint8)
    # add missing axis if omitted
    if len(im.shape) == 2:
        im = im[:,:,None]
    # resolve alpha channel
    if im.shape[2] == 4:
        im = (im[:,:,:3].astype(np.float32) * im[:,:,3:].astype(np.float32) / 255.).clip(0., 255.).astype(np.uint8)
    # grayscale to rgb
    if im.shape[2] == 1:
        im = np.repeat(im, 3, axis=2)
    # pad a final line if number of rows is odd
    if im.shape[0] % 2:
        im = np.concatenate([im, np.zeros([1, im.shape[1], 3], dtype=np.uint8)], axis=0)
    return im

def tctim(im, bbox=None):
    im = _imgify(im, bbox=bbox)
    return _tctim(im)

def imprint(im, bbox=None, file=stdout, flush=False):
    print(tctim(im, bbox=bbox), file=file, flush=flush)

def imread(fpath, fbacksize=(64, 64)):
    try:
        tsize = get_terminal_size()
        nrow, ncol = 2 * tsize.lines, tsize.columns
    except OSError:
        ncol, nrow = fbacksize

    try:
        im = imopen(fpath)
    except FileNotFoundError as err:
        logger.error(str(err))
        return np.array([])

    im.thumbnail((nrow, ncol))
    return np.asarray(im)

#def montage(images, hnum):
#    (zip([images[ind::hnum] for ind in range(hnum)]))
