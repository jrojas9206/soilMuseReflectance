import os 
import cv2
from pathlib import Path
import matplotlib.pyplot as plt 
from srmouse.processor import ReflectancePointLoader
from srmouse.processor import LoadMeasurements
from srmouse.viz import plotReflectanceSignature
from srmouse.viz import plotReflectanceSignatures
from srmouse.processor import SpectralCube
from srmouse.imageTools import manualCropPetriDishe
from srmouse.viz import histSoilSample
from srmouse.viz import showManualPoint

root = str(Path(__file__).parent.absolute())
path2test = Path(os.path.join(root, 
                 "../../data/CPR-ATL-KET_control/Data/Spectrum_Data.txt")).resolve()
path2spectralCube = Path(os.path.join(root,
                         '../../data/CPR-ATL-KET_control/Spectral_Cube/')).resolve()
path2rgbImage = Path(os.path.join(root,
                     '../../data/CPR-ATL-KET_control/Images/RGB_image.png')).resolve()
path2measurements = Path(os.path.join(root,
                         '../../data/')).resolve()

def test_reflectancePointLoader():
    oRP = ReflectancePointLoader(path2test)
    df = oRP.getResults().head()
    plotReflectanceSignature(df,
                             idx2skip=0,
                             title='Soil Reflectance Signature: CPR-ATL-KET_control',
                             avgPlot=True)

test_reflectancePointLoader()

lstValues, lstNames = LoadMeasurements(path2measurements)

plotReflectanceSignatures(lstValues, 
                        idx2skip=0,
                        avgPlot=True, 
                        filesNames=lstNames)

sc_ex = SpectralCube(path2spectralCube)

df = sc_ex.getSignature([[500, 500], [1000, 1000]], cSize=2)

plotReflectanceSignature(df,
                         title='Soil Reflectance Signature: CPR-ATL-KET_control',
                         ylabel='Pixel Values',
                         avgPlot=False)


img = cv2.imread(path2rgbImage, cv2.COLOR_BGR2RGB)

showManualPoint(img,
                [[500, 500], [1000, 1000]])

segmented = manualCropPetriDishe(img,
                     [500, 500],
                     100,
                     False,
                     )

mask = manualCropPetriDishe(img,
                     [500, 500],
                     100,
                     True,
                     )

mImg = sc_ex.getCube()

histSoilSample(mImg, 
               mask, 
               legend=sc_ex.getBands())
plt.figure()
plt.imshow(img)
plt.figure()
plt.imshow(segmented)
plt.show()