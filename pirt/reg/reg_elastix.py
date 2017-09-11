""" Registration using the elastix registration toolkit.
"""

from .reg_base import AbstractRegistration
from pirt.utils import ssdf 
from pirt import DeformationFieldBackward
from .pyelastix import Elastix


class ElastixRegistration(AbstractRegistration):
    """ ElastixRegistration(im1, im2)
    
    Registration class for registration using the Elastix toolkit.
    [http://elastix.isi.uu.nl/]
    
    Introduction
    ------------
    This class performs a bspline transformation by default. See also
    the convenience classes ElastixRegistration_*.
    
    The params property this class returns a struct with a few common
    Elastix parameters. the params2 property contains another set of
    more advanced parameters. Note that any parameter known to elastix
    can be added to the parameter structures, which enables tuning the
    registration in great detail. Also note that two parameter structs
    can be combined by adding them. 
    
    Because the parameters directly represent the parameters for the
    Elastix toolkit, their names do not follow the style of most
    other registration objects in this package.
    
    
    Registration parameters 
    -----------------------
    This lists some of the default parameters, for more details
    we refer to the elastix manual.
    
    FinalGridSpacingInPhysicalUnits : int
        When using the BSplineTransform, the final spacing of the grid.
        This controls the smoothness of the final deformation.
    NumberOfResolutions : int
        Most registration algorithms adopt a multiresolution approach
        to direct the solution towards a global optimum and to speed
        up the process. This parameter specifies the number of scales
        to apply the registration at. (default 4)
    MaximumNumberOfIterations  : int
        Maximum number of iterations in each resolution level.
        200-2000 works usually fine for nonrigid registration.
        The more, the better, but the longer computation time.
        This is an important parameter! (default 500)
    
    """
    transformation_type = 'bspline'
    
    def __init__(self, *args):
        AbstractRegistration.__init__(self, *args, makeFloat=True)
        
        # Check
        if not isinstance(self, ElastixGroupwiseRegistration):
            if len(args)>2:
                raise ValueError('Can only register two images. '
                                 'Use ElastixGroupwiseRegistration instead.')
        
        reg = Elastix()
        self._params2 = ssdf.new() + reg.get_advanced_params()    
    
    
    def _defaultParams(self):
        """ Overload to create all default params.
        """
        params = AbstractRegistration._defaultParams(self)
        params.mapping = 'backward'
        
        reg = Elastix()
        params += reg.get_default_params(self.transformation_type)
        return params
    
    @property
    def params2(self):
        return self._params2
    
    
    def register(self, verbose=1, fig=None):
        """ register()
        
        Perform the registration. 
        
        """
        
        # Compile params
        params = self.params2 + self.params
        
        # Get images
        if isinstance(self, ElastixGroupwiseRegistration):
            im1, im2 = self._ims, None
        else:
            im1, im2 = self._ims[0], self._ims[1]
        
        # Use elastix
        reg = Elastix()
        im, fields = reg.register(im1, im2, params, verbose=verbose)
        
        
        for i in range(len(fields)):
            field = fields[i]
            
            # Reverse (Elastix uses x-y-z order)
            field = [f for f in reversed(field)]
            
            # Set resulting deforms
            self._deforms[i] = DeformationFieldBackward(*field)
        
        # Also set deformed image
        self._deformed_image = im
    
    
    def get_elastix_deformed_image(self):
        """ get_elastix_deformed_image()
        
        Get the deformed input image found as Elastix created it. This 
        should be the same (except for small interpolation errors) to 
        the image obtained using reg.get_deformed_image(0).
        
        """
        
        # Check if result is set
        if not self._deforms:
            raise RuntimeError('The result is not available; run register().')
        
        # Return
        return self._deformed_image
    


class ElastixRegistration_affine(ElastixRegistration):
    """ 
    
    Registration class for registration using the Elastix toolkit.
    [http://elastix.isi.uu.nl/]
    
    This class performs an affine transformation by default. See
    the ElastixRegistration class for more details.
    
    
    Registration parameters 
    -----------------------
    This lists some of the default parameters, for more details
    we refer to the elastix manual.
    
    AutomaticScalesEstimation : bool
        When using a rigid or affine transform. Scales the affine matrix
        elements compared to the translations, to make sure they are in
        the same range. In general, it's best to use automatic scales
        estimation.
    AutomaticTransformInitialization : bool
        When using a rigid or affine transform. Automatically guess an
        initial translation by aligning the geometric centers of the 
        fixed and moving.
    NumberOfResolutions : int
        Most registration algorithms adopt a multiresolution approach
        to direct the solution towards a global optimum and to speed
        up the process. This parameter specifies the number of scales
        to apply the registration at. (default 4)
    MaximumNumberOfIterations  : int
        Maximum number of iterations in each resolution level.
        200-2000 works usually fine for nonrigid registration.
        The more, the better, but the longer computation time.
        This is an important parameter! (default 500)
    
    """
    transformation_type = 'affine'



class ElastixRegistration_rigid(ElastixRegistration):
    """ 
    
   Registration class for registration using the Elastix toolkit.
    [http://elastix.isi.uu.nl/]
    
    This class performs a rigid transformation by default. See
    the ElastixRegistration class for more details.
    
    
    Registration parameters 
    -----------------------
    This lists some of the default parameters, for more details
    we refer to the elastix manual.
    
    AutomaticScalesEstimation : bool
        When using a rigid or affine transform. Scales the affine matrix
        elements compared to the translations, to make sure they are in
        the same range. In general, it's best to use automatic scales
        estimation.
    AutomaticTransformInitialization : bool
        When using a rigid or affine transform. Automatically guess an
        initial translation by aligning the geometric centers of the 
        fixed and moving.
    NumberOfResolutions : int
        Most registration algorithms adopt a multiresolution approach
        to direct the solution towards a global optimum and to speed
        up the process. This parameter specifies the number of scales
        to apply the registration at. (default 4)
    MaximumNumberOfIterations  : int
        Maximum number of iterations in each resolution level.
        200-2000 works usually fine for nonrigid registration.
        The more, the better, but the longer computation time.
        This is an important parameter! (default 500)
    
    """
    transformation_type = 'rigid'


class ElastixGroupwiseRegistration(ElastixRegistration):
    """ ElastixGroupwiseRegistration(*images)
    
    Registration class for registration using the Elastix toolkit.
    [http://elastix.isi.uu.nl/]
    
    This variant uses the groupwise registration approach as proposed
    by Metz et al. "Nonrigid registration of dynamic medical imaging data
    using nD+t B-splines and a groupwise optimization approach"
    
    Introduction
    ------------
    
    The params property this class returns a struct with a few common
    Elastix parameters. the params2 property contains another set of
    more advanced parameters. Note that any parameter known to elastix
    can be added to the parameter structures, which enables tuning the
    registration in great detail. Also note that two parameter structs
    can be combined by adding them. 
    
    Because the parameters directly represent the parameters for the
    Elastix toolkit, their names do not follow the style of most
    other registration objects in this package.
    
    
    Registration parameters 
    -----------------------
    This lists some of the default parameters, for more details
    we refer to the elastix manual.
    
    FinalGridSpacingInPhysicalUnits : int
        When using the BSplineTransform, the final spacing of the grid.
        This controls the smoothness of the final deformation.
    NumberOfResolutions : int
        Most registration algorithms adopt a multiresolution approach
        to direct the solution towards a global optimum and to speed
        up the process. This parameter specifies the number of scales
        to apply the registration at. (default 4)
    MaximumNumberOfIterations  : int
        Maximum number of iterations in each resolution level.
        200-2000 works usually fine for nonrigid registration.
        The more, the better, but the longer computation time.
        This is an important parameter! (default 500)
    
    """
    pass
