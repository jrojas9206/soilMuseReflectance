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


img = cv2.imread('/home/pablo/Documents/repos/soilMuseReflectance/data/CPR-ATL-KET_control/Images/RGB_image.png', cv2.COLOR_BGR2RGB)
print(img.dtype)
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

print(mImg.shape)

histSoilSample(mImg, 
               mask, 
               legend=sc_ex.getBands())
plt.show()
# plt.figure()
# plt.imshow(img)
# plt.figure()
# plt.imshow(segmented)
# plt.show()