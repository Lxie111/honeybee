# coding=utf-8
"""dctimestep - transform a RADIANCE scene description"""

from _commandbase import RadianceCommand
from ..datatype import RadiancePath,RadianceValue
from ..parameters.dctimestep import DctimestepParameters

import os

class Dctimestep(RadianceCommand):
    #It makes sense to always use the outputFileNameFormat input to specify the
    # output file instead of using the stdout parameter.
    vmatrixSpec = RadianceValue('vmatrix','V matrix specification')
    tmatrixFile = RadiancePath('tmatrix','T matrix XML file')
    dmatrixFile = RadiancePath('dmatrix','D matrix file')
    skyVectorFile = RadiancePath('skyVectorFile', 'sky vector file',
                                 relativePath=None)
    outputFileName = RadiancePath('outputFile','output file name',
                                  relativePath=None)
    daylightCoeffSpec = RadiancePath('dayCoeff',
                                     'Daylight Coefficients Specification')

    def __init__(self,tmatrixFile=None,dmatrixFile=None,skyVectorFile=None,
                 vmatrixSpec=None,dctimestepParameters=None,
                 outputFilenameFormat=None,outputFileName=None,
                 daylightCoeffSpec=None):
        RadianceCommand.__init__(self)

        self.vmatrixSpec = vmatrixSpec
        self.tmatrixFile = tmatrixFile
        self.dmatrixFile = dmatrixFile
        self.skyVectorFile = skyVectorFile
        self.dctimestepParameters = dctimestepParameters
        self.outputFilenameFormat = outputFilenameFormat
        self.outputFileName = outputFileName
        self.daylightCoeffSpec = daylightCoeffSpec

    @property
    def dctimestepParameters(self):
        """Get and set gendaymtxParameters."""
        return self.__dctimestepParameters
    
    
    @dctimestepParameters.setter
    def dctimestepParameters(self, parameters):
        self.__dctimestepParameters = parameters if parameters is not None \
            else DctimestepParameters()
    
        assert hasattr(self.dctimestepParameters, "isRadianceParameters"), \
            "input dctimestepParameters is not a valid parameters type."

    @property
    def outputFilenameFormat(self):
        return self._outputFilenameFormat

    @outputFilenameFormat.setter
    def outputFilenameFormat(self,value):
        #TODO: Add testing logic for this !
        if value:
            self._outputFilenameFormat = value
        else:
            self._outputFilenameFormat = None

    def toRadString(self, relativePath=False):
        cmdPath = self.normspace(os.path.join(self.radbinPath, 'dctimestep'))
        vmatrix = self.vmatrixSpec.toRadString().replace('-vmatrix','')
        tmatrix = self.normspace(self.tmatrixFile.toRadString())
        dmatrix = self.normspace(self.dmatrixFile.toRadString())
        threePhaseInputs = vmatrix and tmatrix and dmatrix
        skyVector = self.normspace(self.skyVectorFile.toRadString())
        dctimestepParam = self.dctimestepParameters.toRadString()
        opFileFmt = self.outputFilenameFormat
        outputFileNameFormat = '-o %s'%opFileFmt if opFileFmt else ''
        outputFileName = self.normspace(self.outputFileName.toRadString())
        outputFileName = '> %s'%outputFileName if outputFileName else ''
        daylightCoeffSpec = self.normspace(self.daylightCoeffSpec.toRadString())


        assert not (threePhaseInputs and daylightCoeffSpec),\
        'The inputs for both daylight coefficients as well as the 3 Phase method' \
        ' have been specified. Only one of those methods should be used for ' \
        'calculation at a given time. Please check your inputs.'

        addToStr = lambda val: "%s "%val if val else ''

        #Creating the string this way because it might change again in the
        # future.
        radString = "%s "%cmdPath
        radString += addToStr(dctimestepParam)
        radString += addToStr(outputFileNameFormat)
        radString += addToStr(vmatrix)
        radString += addToStr(tmatrix)
        radString += addToStr(dmatrix)
        radString += addToStr(daylightCoeffSpec)
        radString += addToStr(skyVector)
        radString += addToStr(outputFileName)

        self.checkInputFiles(radString)
        return radString

    @property
    def inputFiles(self):
        dcInput = self.daylightCoeffSpec.toRadString()
        if dcInput:
            return self.skyVectorFile.toRadString(),
        else:
            return (self.tmatrixFile.toRadString(),self.dmatrixFile.toRadString(),
                    self.skyVectorFile.toRadString())