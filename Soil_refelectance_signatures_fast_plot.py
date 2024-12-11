import os 
import cv2
import sys 
from pathlib import Path 
from matplotlib import pyplot as plt

from srmouse.processor import LoadMeasurements
from srmouse.viz import plotReflectanceSignatures

path_to_folder = str(input("Write here the full path to your folder with camera's data: " ))  # Write here the full path to folder with your data acquired with MUSES9 multispectral camera

path2measurements = Path(os.path.join(f"{path_to_folder}/")).resolve()  

lstValues, lstNames = LoadMeasurements(path2measurements)

plotReflectanceSignatures(lstValues, 
                          idx2skip=0, 
                          avgPlot=True, 
                          filesNames=lstNames)

plt.savefig("Reflectance_Signatures_results.png", dpi=150)
