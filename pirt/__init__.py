""" Pirt - Python Image Registration Toolkit.

Pirt provides functionality for image registration. It is the result
of my PhD. There is functionality for a variety of image registration
algorothms. Most notably pirt provides an easy way to use the Elastix
toolkit. Further it implements some algorithms in Cython (Demons and
Gravity).

Image registration itself requires several image processing techniques
and data types, which are also included in this package:

  * pirt.utils.gaussfun - function for Gaussian smoothing and
    derivatives, image pyramid class
  * pirt.interp - interpolation of 1D, 2D and 3D data (nearest, linear,
    and various spline interpolants)
  * pirt.splinegrid - defines a B-spline grid class (for data up to
    three dimensions) and a class to describe a deformation grid
    (consisting of a B-spline grid for each dimension)
  
The registration algoriths are in `pirt.reg`.

"""

from __future__ import absolute_import, print_function, division 


# Set version number
__version__ = '2.0'


from pirt.utils import Point, Pointset, Aarray

from pirt.utils.gaussfun import (gaussiankernel, gfilter, gfilter2,
                                 diffusionkernel, diffuse, diffuse2)
from pirt.utils.pyramid import ScaleSpacePyramid

from . import interp

from pirt.splinegrid import SplineGrid, GridContainer, FieldDescription, FD
from pirt.deformation import (Deformation, DeformationIdentity, 
                              DeformationGrid, DeformationField,
                              DeformationGridForward, DeformationFieldForward,
                              DeformationGridBackward, DeformationFieldBackward)

from .utils.randomdeformations import create_random_deformation, RandomDeformations
