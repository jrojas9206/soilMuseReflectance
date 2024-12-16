import cv2
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

def plotReflectanceSignature(df:pd.DataFrame, xlabel:str="Bands (nm)", ylabel:str="Reflectance", 
                             title:str='Soil Reflectance Signature', idx2skip:list=[],
                             avgPlot:bool=False, savePlot:str=None) -> None:
    '''
        Plot the reflectance values sorted in the dataframe 
        in the row it is expected a measurement point and in the columns 
        each of the bands related to point 

        Parameters
        -----------
            df : pandas.DataFrame, DataFrame with the different reflectance measurements 
            xlabel : str, Name to set in the x-axis 
            ylabel : str, Name to set in the y-Axis 
            title : str, Plot title
            idx2skip : list, List of dataframe index to skip, Default []
            avgPlot : bool, If true the avarange all the signatures will be displayed. Default False 
            savePlot : str, Path and filename to save the plot e.g: /home/reflectanceSignature.png. Default None 
    '''
    plt.figure()
    bandNames = []
    bandValues = []
    if avgPlot:
        for colName in df.columns.tolist():
            if idx2skip >= 0:
                bandValues.append(df.iloc[ [i for i in range(df.shape[0]) if i != idx2skip] ][colName].mean())
            else:
                bandValues.append(df[colName].mean())
            bandNames.append(colName)
        plt.plot(range(len(bandNames)), 
                    bandValues)
        
    else:
        for idx in range(df.shape[0]):
            if idx in idx2skip:
                continue
            measuredPoint = df.loc[idx]
            bandNames = list(measuredPoint.index)
            bandValues = list(measuredPoint.values) 
            plt.plot(range(len(bandNames)), 
                    bandValues)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(range(len(bandNames)),
               bandNames)
    plt.title(title)
    plt.tight_layout()
    if not isinstance(savePlot, type(None)):
        plt.savefig(savePlot, dpi=300)

def plotReflectanceSignatures(dfList:list, idx2skip:list=[], xlabel:str="Bands (nm)", ylabel:str="Reflectance", 
                             title:str='Soil Reflectance Signature',avgPlot:bool=False, legend:list=None, 
                             savePlot:str=None) -> None:
    """
        Plot a list of reflectance measurements from different areas 

        Parameters 
        -----------
            dfList : list, List of pandas DataFrames, the column of each dataframe are the bands and the rows the measured points
            idx2skip : list, List of index to skip
            xlabel : str, Name of the x-axis. Default "Bands (nm)" 
            ylabel : str, Name of the y-axis. Default "Reflectance"
            title : str, plot title. Default 'Soil Reflectance Signature'
            avgPlot : bool, If true the averga plot of all the signature will be displayed. Default False 
            legend : list, List of strings use to display as plot legends  
            savePlot : str, Path and filename to save the plot e.g: /home/reflectanceSignature.png. Default None 
    """
    if(len(dfList) != len(legend)):
        raise ValueError("List length of dfList and filesNames is different. They must be the same length")
    listLegends = []
    bandValues = []
    bandNames = []
    for idxFiles, measuredPoints in enumerate(dfList):
        bandValues = []
        bandNames = []
        if avgPlot:
            for colName in measuredPoints.columns.tolist():
                if idx2skip >= 0:
                    bandValues.append(measuredPoints.iloc[ [i for i in range(measuredPoints.shape[0]) if i != idx2skip] ][colName].mean())
                else:
                    bandValues.append(measuredPoints[colName].mean())
                bandNames.append(colName)
            plt.plot(range(len(bandNames)), 
                        bandValues)
            if len(legend) == len(dfList):
                listLegends.append("%s" %(legend[idxFiles]))
        else:
            for idx in range(measuredPoints.shape[0]):
                if idx2skip >= 0 and idx2skip == idx:
                    continue
                measuredPoint = measuredPoints.loc[idx]
                bandNames = list(measuredPoint.index)
                bandValues = list(measuredPoint.values) 
                plt.plot(range(len(bandNames)), 
                        bandValues)
                if len(legend) == len(dfList):
                    listLegends.append("%s-%i" %(legend[idxFiles], idx))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(range(len(bandNames)),
               bandNames)
    plt.title(title)
    if len(legend) == len(dfList):
        plt.legend(listLegends)
    plt.tight_layout()
    if not isinstance(savePlot, type(None)):
        plt.savefig(savePlot, dpi=300)

def histSoilSample(img:np.array, mask:np.array, bins:int=20, value2keep:float=255, legend:list=[], 
                   xlabel:str='Pixel Values', ylabel:str='Frequency', title:str="Bands Histogram", 
                   savePlot:str=None) -> None:
    '''
        Plot the histogram related to object of interest 

        Parameters 
        -----------
            img : numpy.array, Image of size (N,M,CH)
            mask : numpy.array, Binary mask of size (N,M)
            bins : int, Number of bins to plot. Default 20 
            values2keep : int, Number that represent the integer that must be keep it from the referenced mask. Default 255 
            legend : list, List of string to display as legeneds. Default []
            xlabel : str, Name of the x-axis. Default 'Pixel Values'
            ylabel : str, Name of the y-axis. Default 'Frequency'
            title : str, Plot title. Default 'Bands Histogram'
            savePlot : str, Path and filename to save the plot e.g: /home/reflectanceSignature.png. Default None 

    '''
    idx2keep = np.where(mask == value2keep)
    _, edges = np.histogram(img, 
                            bins=bins)
    channels = img.shape[2]
    plt.figure()
    for idx in range(channels):
        cImage = img[:, :, idx]
        objIterest = cImage[idx2keep].reshape(-1,1)
        plt.hist(objIterest, 
                 bins=edges, alpha=0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    if len(legend) == img.shape[2]:
        plt.legend(legend)
    if not isinstance(savePlot, type(None)):
        plt.savefig(savePlot, dpi=300)

def showManualPoint(image:np.array, points:list, cross:int=100, thinkness:int=5, returnImage:bool=False):
    '''
        Display the coordinates from where the signatures were obtained 

        Parameters 
        -----------
            image : numpy.array, Image with shape (N,M,CH)
            points : list, List of tuples, each tuple contain (X,Y) coordinates 
            cross : int, Size in pixell to display the cross marker. Default 100  
            thinkness : int, Line thinkness in pixels. Default 5
            returnImage : bool, if True the method will return a numpy array of size (N,M,3)
    '''
    img = image.copy()
    for point in points:
        img = cv2.line(img, 
                (point[0]-cross, point[1]-cross), 
                (point[0]+cross, point[1]+cross), 
                (0, 0, 255),
                thickness=thinkness) 
        img = cv2.line(img, 
                (point[0]+cross, point[1]-cross), 
                (point[0]-cross, point[1]+cross), 
                (0, 0, 255), 
                thickness=thinkness)
    if returnImage:
        return img
    plt.imshow(img) 
    