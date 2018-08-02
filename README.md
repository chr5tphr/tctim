# True-Color Terminal Image visualization library for Python

A tool to view images or matrices directly in your (true-color supporting) terminal.
Great for debugging purposes!

Example in Python:
```python
import numpy as np
from tctim import imprint

# make some data to visualize
grid = np.stack(np.meshgrid(np.arange(32),np.arange(32)))
dist = ((np.array([15.5, 15.5])[:,None,None] - grid)**2).sum(axis=0)**.5

# print to console
imprint(dist)

# make some colorful data
col = np.stack([np.zeros_like(dist), dist, -dist], axis=-1)
imprint(col)

#================================
# save file to read later with CLI
from imageio import imsave

# rescale data
lo, hi = col.min(), col.max()
img = ((col - lo) * 255./(hi-lo)).clip(0., 255.).astype(np.uint8)
imsave('/tmp/someimage.png', img)
```

There is also a commandline-interface included:
```shell
$ tctim /tmp/someimage.png
```

## Note:
There is no limit for maximum image sizes implemented, so be careful which images you print to terminal!
I head my terminal glitch out after I printed a rather large image.
