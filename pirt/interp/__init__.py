""" Module interp

Exposes several functions for interpolation, implemented in Cython.
This code is part of pirt, but written to be easily made stand-alone,
or be made a subpackage of another package.

Copyright 2014(C) Almar Klein

"""

from __future__ import absolute_import, print_function, division 

import os

# Need some stuff from pirt utils. These can easily be transfered if necessary
from pirt.utils import Point, Aarray
from pirt.utils.gaussfun import diffuse

# Import cython module
if os.getenv('PIRT_USE_PYXIMPORT', False):
    # Compile on the fly (for use during development)
    import pyximport  # from Cython
    pyximport.install()
from . import interpolation_

# Import cython part
from .interpolation_ import interp, project, ainterp, aproject
from .interpolation_ import make_samples_absolute, fix_samples_edges
from .interpolation_ import get_cubic_spline_coefs, meshgrid

# Import user-friendly functions
from .func import deform_backward, deform_forward
from .func import resize, imresize
from .func import zoom, imzoom

from .sliceinvolume import SliceInVolume
