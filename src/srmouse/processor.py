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
    def __init__(self, iPath2file:str=None) -> None:
        self._path2file = str(iPath2file)
        self._dfMeasurements = None
        if iPath2file is not None:
            self.__loadTxtFile()

    def setPath(self, iPath2File:str) -> None:
        self._path2file = str(iPath2File)
        self.__loadTxtFile()

    def getPath(self) -> str:
        return self._path2file()
    
    def getSetName(self, separator:str='/'):
        return self._path2file.split(separator)[-3]

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
    
def LoadMeasurements(rootFolder:str, skipFolder:str='Calibration', subPath:str='Data') -> list:
    """
        Load a set of measurements 
    
        :Args:
            :rootFolder: str, Absolute path to the folder with the measurements
            :skipFolder: str, Measurement folder to not take into acount
            :subPath: str, Sub folder where the reflectance measurements are located 
    """
    listDirectories = [os.path.join(rootFolder, folderName, subPath) for folderName in os.listdir(rootFolder) if folderName != skipFolder]
    dfList = []
    dfNames = []
    for folder in listDirectories:
        file2load = [os.path.join(folder,i) for i in os.listdir(folder) if '.txt' in i]
        if len(file2load) == 0:
            continue
        file2load = file2load[0]
        oRP = ReflectancePointLoader(file2load)
        dfList.append(oRP.getResults())
        dfNames.append(oRP.getSetName())
    return dfList, dfNames

class SpectralCube:

    def __init__(self, path:str=None, imgExtension:str='jpg', cSize:int=2) -> None:
        self._path = path 
        self._bands = []
        self._extension = f'.{imgExtension}'
        self._mImage = np.array([])
        self._cSize = cSize
        self.__loadCube()

    def __loadCube(self) -> None:
        '''
            Load the multispectral images 
        '''
        name2band = lambda fileName: fileName.split('.')[0][5:]
        lstFileNames = [fileName for fileName in os.listdir(self._path) if self._extension in fileName]
        # Sort the spectrum from min to max 
        bands = [int(name2band(fileName)) for fileName in lstFileNames]
        zNamesBands = zip(bands, lstFileNames)
        zNamesBands = sorted(zNamesBands)
        lstFileNames, sBands = [i for _, i in zNamesBands], [i for i, _ in zNamesBands] 
        # Create a tensor 
        lstImages = []
        for cFile in lstFileNames:
            path2file = os.path.join(self._path, cFile)
            cImage = cv2.imread(path2file,
                                cv2.IMREAD_GRAYSCALE)
            lstImages.append(cImage)
        self._mImage = np.dstack(lstImages)
        self._bands = sBands

    def getSignature(self, coordinatesXY:list,  cSize:int=-1) -> pd.DataFrame:
        '''
            Get the signature of several point from the captured images 

            :Args:
                :coordinatesXY: list, List of list, each of the list must contain the coordinates XY of iterest. e.g [[x0,y0], [x1,y1], ...]
            :Return:
                pandas.DataFrame
        '''
        if len(coordinatesXY) != 2:
            raise ValueError('Expected list length 2 got %i' %(len(coordinatesXY)))
        size2set = 1
        if cSize <= 0:
            size2set = self._cSize
        else:
            size2set = cSize
        if len(coordinatesXY) <= 0:
            raise ValueError('The coordinate list is empty!') 
        tmpDict = {}
        for coordinate in coordinatesXY:   
            if coordinate[0]+size2set >= self._mImage.shape[0] or coordinate[1]+size2set >= self._mImage.shape[0]:
                raise ValueError('Selected pixel coordinates outside the image')
            signature = self._mImage[coordinate[0]:coordinate[0]+size2set, coordinate[1]:coordinate[1]+size2set, :]
            for idxBand, bandName in enumerate(self._bands):
                pixelsAvg = np.mean(signature[:,:,idxBand])
                if str(bandName) not in tmpDict.keys():
                    tmpDict[str(bandName)] = [pixelsAvg]
                else:
                    tmpDict[str(bandName)].append(pixelsAvg)
        return pd.DataFrame.from_dict(tmpDict) 

    def getCube(self):
        return self._mImage