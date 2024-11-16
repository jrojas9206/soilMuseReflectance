import os 
import sys 
import cv2
import warnings 
import numpy as np
import pandas as pd 

class ReflectancePointLoader():
    '''
        Class to load and sort txt file with the 
        reflectande measurements from the Muse Software 
    '''
    def __init__(self, iPath2file:str=None, bands:int=12) -> None:
        self._path2file = iPath2file
        self._dfMeasurements = None
        self._bands = bands
        if iPath2file is not None:
            self.__loadTxtFile()

    def setPath(self, iPath2File:str) -> None:
        self._path2file = iPath2File
        self.__loadTxtFile()

    def getPath(self) -> str:
        return self._path2file()

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
        return self._dfMeasurements
    
    def getBands(self) -> list:
        '''
            Return the bands spectrum available in the file
        '''
        return np.unique(self._dfMeasurements.columns.tolist())
    
class LoadMeasurements():

    def __init__(self, rootFolder:str, skipFolder:str='Calibration'):
        """
            :Args:
                :rootFolder: str, Absolute path to the folder with the measurements
                :skipFolder: str, Measurement folder to not take into acount
        """
        listDirectories = [os.path.join(rootFolder, folderName) for folderName in os.listdir(rootFolder) if folderName != skipFolder]
        