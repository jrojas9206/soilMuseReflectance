import pandas as pd 
import matplotlib.pyplot as plt 

def plotReflectanceSignature(df:pd.DataFrame, xlabel:str="Bands (nn)", ylabel:str="Reflectance", 
                             title:str='Soil Reflectance Signature', idx2skip:int=-1,
                             avgPlot:bool=False) -> None:
    '''
        Plot the reflectance values sorted in the dataframe 
        in the row it is expected a measurement point and in the columns 
        each of the bands related to point 

        :Args:
            :df:  pandas.DataFrame, DataFrame with the different reflectance measurements 
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
            if idx2skip >= 0 and idx2skip == idx:
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

def plotReflectanceSignatures(dfList:list, idx2skip:int=-1, xlabel:str="Bands (nn)", ylabel:str="Reflectance", 
                             title:str='Soil Reflectance Signature',avgPlot:bool=False, filesNames:list=None) -> None:
    """
        Plot a list of reflectance meqsurements from different areas 

        :Args:
            :dfList: list, List of pandas DataFrames, the column of each dataframe are the bands and the rows the measured points
    """
    if(len(dfList) != len(filesNames)):
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
            if len(filesNames) == len(dfList):
                listLegends.append("%s" %(filesNames[idxFiles]))
        else:
            for idx in range(measuredPoints.shape[0]):
                if idx2skip >= 0 and idx2skip == idx:
                    continue
                measuredPoint = measuredPoints.loc[idx]
                bandNames = list(measuredPoint.index)
                bandValues = list(measuredPoint.values) 
                plt.plot(range(len(bandNames)), 
                        bandValues)
                if len(filesNames) == len(dfList):
                    listLegends.append("%s-%i" %(filesNames[idxFiles], idx))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(range(len(bandNames)),
               bandNames)
    plt.title(title)
    if len(filesNames) == len(dfList):
        plt.legend(listLegends)
    plt.tight_layout()