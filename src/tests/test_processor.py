import os 
from pathlib import Path
import matplotlib.pyplot as plt 
from srmouse.processor import ReflectancePointLoader

root = str(Path(__file__).parent.absolute())
path2test = Path( os.path.join(root, 
                               "../../data/CPR-ATL-KET_control/Data/Spectrum_Data.txt")).resolve()

def test_reflectancePointLoader():
    oRP = ReflectancePointLoader(path2test)
    df = oRP.getResults().head()
    seriesCalibration = df.loc[0]
    idx = seriesCalibration.index 
    values = seriesCalibration.values

    seriesPoint0 = df.loc[1]
    idx0 = seriesPoint0.index
    values0 = seriesPoint0.values
    plt.plot(idx, values)
    plt.plot(idx0, values0)
    plt.xlabel('Wavelenght (nn)')
    plt.ylabel('Amplitude')
    plt.title('Soil reflectance test')
    plt.show()

test_reflectancePointLoader()