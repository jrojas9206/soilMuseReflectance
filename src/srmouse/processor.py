import os 
import sys 
import cv2
import numpy 
import warnings 
import pandas as pd 

class ReflectancePointLoader():
    '''
        Class to load and sort txt file with the 
        reflectande measurements from the Muse Software 
    '''
    def __init__(self, iPath2file:str, bands:int=12) -> None:
        self._path2file = iPath2file
        self._dfMeasurements = None
        self._bands = bands

    def __loadTxtFile(self):
        '''
            Load the txt file with the reflectance measurements 
        '''
        tmpDict = {} # Temporal dictionary to keep the band measurements 
        with open(self._path2file, 'r') as oFile:
            for idx, cLine in enumerate(oFile.readlines()):
                try:
                    cBand_nn, cReflectance = cLine.split(',')
                except ValueError:
                    warnings.warn(f'On {idx} the data did not have the formar band,reflectanceValue. Please verify the loaded file')
                    continue
                try:
                    value2keep = float(cReflectance)
                except ValueError:
                    warnings.warn('The expected reflectance value is not numeric. Verify file index {idx}.')
                    continue
                if cBand_nn not in tmpDict.keys():
                    tmpDict[cBand_nn] = [value2keep]
                else:
                    tmpDict[cBand_nn].append(value2keep)
        self._dfMeasurements = pd.DataFrame.from_dict(tmpDict)

    def getResults(self) -> pd.DataFrame:
        '''
            Return the dataframe with the sorted band's reflectance
        ''' 
        self.__loadTxtFile()
        return self._dfMeasurements