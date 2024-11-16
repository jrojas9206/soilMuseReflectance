import os 
from pathlib import Path
import matplotlib.pyplot as plt 
from srmouse.processor import ReflectancePointLoader
from srmouse.processor import LoadMeasurements
from srmouse.viz import plotReflectanceSignature
from srmouse.viz import plotReflectanceSignatures

root = str(Path(__file__).parent.absolute())
path2test = Path( os.path.join(root, 
                               "../../data/CPR-ATL-KET_control/Data/Spectrum_Data.txt")).resolve()

def test_reflectancePointLoader():
    oRP = ReflectancePointLoader(path2test)
    df = oRP.getResults().head()
    
    print(oRP.getSetName())
    # plotReflectanceSignature(df,
    #                          idx2skip=0,
    #                          title='Soil Reflectance Signature: CPR-ATL-KET_control',
    #                          avgPlot=True)

test_reflectancePointLoader()

lstValues, lstNames = LoadMeasurements('/home/pablo/Documents/repos/soilMuseReflectance/data')

plotReflectanceSignatures(lstValues, 
                          idx2skip=0,
                          avgPlot=True, 
                          filesNames=lstNames)