import os 
from pathlib import Path
import matplotlib.pyplot as plt 
from srmouse.processor import ReflectancePointLoader
from srmouse.processor import LoadMeasurements
from srmouse.viz import plotReflectanceSignature
from srmouse.viz import plotReflectanceSignatures
from srmouse.processor import SpectralCube

root = str(Path(__file__).parent.absolute())
path2test = Path( os.path.join(root, 
                               "../../data/CPR-ATL-KET_control/Data/Spectrum_Data.txt")).resolve()

def test_reflectancePointLoader():
    oRP = ReflectancePointLoader(path2test)
    df = oRP.getResults().head()
    
    print(oRP.getSetName())
    plotReflectanceSignature(df,
                             idx2skip=0,
                             title='Soil Reflectance Signature: CPR-ATL-KET_control',
                             avgPlot=True)

test_reflectancePointLoader()

lstValues, lstNames = LoadMeasurements('/home/pablo/Documents/repos/soilMuseReflectance/data')

# plotReflectanceSignatures(lstValues, 
#                           idx2skip=0,
#                           avgPlot=True, 
#                           filesNames=lstNames)

sc_ex = SpectralCube('/home/pablo/Documents/repos/soilMuseReflectance/data/CPR-ATL-KET_control/Spectral_Cube')

print(sc_ex.getCube().shape)

df = sc_ex.getSignature([[500, 500], [1000, 1000]], cSize=2)

print(df.head())

plotReflectanceSignature(df,
                         title='Soil Reflectance Signature: CPR-ATL-KET_control',
                         ylabel='Pixel Values',
                         avgPlot=True)

plt.show()