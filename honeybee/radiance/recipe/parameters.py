"""Radiance parameters collection for recipes.


Note on default parameters for daylight coefficient based studies

    1. These parameters are meant specifically for rcontrib-based workflows and are not
        applicable to conventional rpict- and rtrace- based simulations.
    2. The values in tuples DCDEFAULTS, VMDEFAULTS are geared towards illuminance
        simulations. The values for DMDEFAULTS and SMDEFAULTS can be used with
        image-based simulations too.
    3. The value for limit-weight should be a value less than 1/ambient-divisions. The
        current values have been assigned as (1/ambient-divisions)*0.01. This should be
        taken into account if these parameters are being changed in the future.
    4. Finally, in the present scenario, there are no optimized set of parameters to
        bring any simulation results to convergence using Monte-Carlo simulations. So,
        these default values are based on best-practice discussions and experience of
        developers.
"""
from ..parameters.gridbased import GridBasedParameters
from ..parameters.imagebased import ImageBasedParameters
from ..parameters.rcontrib import RcontribParameters
from ..parameters.rfluxmtx import RfluxmtxParameters

from collections import namedtuple

# ~~~~~~~~~~~STARTING DEFAULT PARAMETERS

# Illuminance based daylight-coefficients
# Parameter settings explained contextually:
# Low: Simple room with almost no external geoemtry.
# Medium: Room with some furniture, partitions with some external geometry
# (few buildings).
# High: A room within a sky-scraper with intricate furnitures, complex
# external geometry (complex fins,overhangs etc).
DCDEFAULTS = (
    {'ambientDivisions': 5000, 'ambientBounces': 3, 'limitWeight': 0.000002,
     'samplingRaysCount': 1},
    {'ambientDivisions': 15000, 'ambientBounces': 5, 'limitWeight': 6.67E-07,
     'samplingRaysCount': 1},
    {'ambientDivisions': 25000, 'ambientBounces': 6, 'limitWeight': 4E-07,
     'samplingRaysCount': 1}
)

# Illuminance based daylight-coefficients
# Parameter settings explained contextually:
# Low: Simple room with one or two glazing systems and no furniture.
# Medium: Room with partitions, furnitures etc. but no occluding surfaces for
# calculation grids.
# High: Complex room or envrionment, like an Aircraft cabin (!) with lots
# of detailing and occulding surfaces.
VMDEFAULTS = (
    {'ambientDivisions': 1000, 'ambientBounces': 3, 'limitWeight': 0.00001},
    {'ambientDivisions': 5000, 'ambientBounces': 5, 'limitWeight': 0.00002},
    {'ambientDivisions': 20000, 'ambientBounces': 7, 'limitWeight': 5E-7}
)

# Daylight Matrix
# Parameter settings explained contextually:
# Low: Room is surrounded by virtually no geometry. The glazing system has a clear view
# of the sky.
# Medium: Room is surrounded by some buildings.
# High: Room is surrounded by several shapes..The glazing might not have a direct view
# of the sky.
DMDEFAULTS = (
    {'ambientDivisions': 1024, 'ambientBounces': 2, 'limitWeight': 0.00001,
     'samplingRaysCount': 1000},
    {'ambientDivisions': 3000, 'ambientBounces': 4, 'limitWeight': 3.33E-06,
     'samplingRaysCount': 1000},
    {'ambientDivisions': 10000, 'ambientBounces': 6, 'limitWeight': 0.000001,
     'samplingRaysCount': 1000}
)

# Sun-matrix
# These settings are set such that every solar disc disc in the celestial hemisphere is
# accounted for and participates in shadow testing.
SMDEFAULTS = {'ambientBounces': 0, 'directJitter': 0, 'directCertainty': 1,
              'directThreshold': 0}

# ~~~~~~~~~~~ENDING DEFAULT PARAMETERS

Parameters = namedtuple('Parameters', ['rad', 'vmtx', 'dmtx', 'smtx'])


def getRadianceParametersGridBased(quality, recType):
    """Get Radiance parameters for grid based recipes.

    Args:
        quality: 0 > low, 1 > Medium, 2 > High
        recType: Type of recipe.
            0 > Point-in-time, 1 > Daylight Coeff., 2 > 3Phase, 3 > 5Phase

    Returns:
        radianceParameters, viewMatrixParameters, daylightMatrixParameters,
        sunMatrixParameters
    """

    if recType == 0:
        return Parameters(GridBasedParameters(quality), None, None, None)
    elif recType == 1:
        # daylight matrix
        dmtxpar = RfluxmtxParameters(quality=quality)
        for k, v in DCDEFAULTS[quality].iteritems():
            setattr(dmtxpar, k, v)

        # sun matrix
        sunmtxpar = RcontribParameters()
        for k, v in SMDEFAULTS.iteritems():
            setattr(sunmtxpar, k, v)

        return Parameters(None, None, dmtxpar, sunmtxpar)
    else:
        # view matrix
        vmtxpar = RfluxmtxParameters(quality=quality)
        for k, v in VMDEFAULTS[quality].iteritems():
            setattr(vmtxpar, k, v)

        # daylight matrix
        dmtxpar = RfluxmtxParameters(quality=quality)
        for k, v in DMDEFAULTS[quality].iteritems():
            setattr(dmtxpar, k, v)

        # sun matrix
        sunmtxpar = RcontribParameters()
        for k, v in SMDEFAULTS.iteritems():
            setattr(sunmtxpar, k, v)

        return Parameters(None, vmtxpar, dmtxpar, sunmtxpar)


def getRadianceParametersImageBased(quality, recType):
    """Get Radiance parameters for image based recipes.

    Args:
        quality: 0 > low, 1 > Medium, 2 > High
        recType: Type of recipe.
            0 > Point-in-time, 1 > Daylight Coeff., 2 > 3Phase, 3 > 5Phase

    Returns:
        radianceParameters, viewMatrixParameters, daylightMatrixParameters
    """
    if recType == 0:
        return Parameters(ImageBasedParameters(quality), None, None, None)
    elif recType == 1:
        # this is a place holder.
        # daylight matrix
        dmtxpar = RfluxmtxParameters(quality=quality)
        for k, v in DCDEFAULTS[quality].iteritems():
            setattr(dmtxpar, k, v)

        # sun matrix
        sunmtxpar = RcontribParameters()
        for k, v in SMDEFAULTS.iteritems():
            setattr(sunmtxpar, k, v)

        return Parameters(None, None, dmtxpar, sunmtxpar)
    else:
        # view matrix
        vmtxpar = RfluxmtxParameters(quality=quality)
        for k, v in VMDEFAULTS[quality].iteritems():
            setattr(vmtxpar, k, v)

        # daylight matrix
        dmtxpar = RfluxmtxParameters(quality=quality)
        for k, v in DMDEFAULTS[quality].iteritems():
            setattr(dmtxpar, k, v)

        # sun matrix
        sunmtxpar = RcontribParameters()
        for k, v in SMDEFAULTS.iteritems():
            setattr(sunmtxpar, k, v)

        return Parameters(None, vmtxpar, dmtxpar, sunmtxpar)
