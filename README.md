# True-Color Terminal Image visualization library for Python

A tool to view images or matrices directly in your (true-color supporting) terminal.
Great for debugging purposes!

It can visualize (`imprint`) or convert to an image representation (`imgify`) anything that
* can be cast into a float- or int- numpy array using `numpy.array` and
* has 2 dimensions (grayscale) or
* has 3 dimensions where the 1, 3 or 4 color channels (grayscale/ RGB/ RGBA) come first or last.

## Install using pip
```shell
$ pip install 'git+git://github.com/chr5tphr/tctim'
```

## Usage
Example in Python:
```python
import numpy as np
from tctim import imprint

# make some data to visualize
grid = np.mgrid[:32, :32]
dist = ((np.array([15.5, 15.5])[:,None,None] - grid)**2).sum(axis=0)**.5

# print to console
imprint(dist)

# make some colorful data
col = np.stack([np.zeros_like(dist), dist, -dist], axis=-1)
imprint(col)

# ================================
# save file to visualize externally or read later with CLI
from PIL import Image
from tctim import imgify

uint8_array = imgify(col)
image = Image.fromarray(uint8_array)
image.save('someimage.png')
```

A command-line interface is included:
```shell
$ tctim someimage.png
```
