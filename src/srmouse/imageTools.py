import os 
import sys 
import cv2
import numpy as np 
import pandas as pd 

def manualCropPetriDishe(img:np.array, circleCenter:list, circleRadius:int, returnMask:bool=False, color:tuple=(255, 255, 255)) -> np.array:
    '''
        Return the manually segmented petri dish 

        :Args:
            :img: numpy.array, Array with the image that contains the object of iterest
            :circleCenter: list, List with the center coordinates (x,y) of the circle
            :circleRadius: int, Circle radius  
        :Return:
            np.array
    '''
    imageSize = img.shape[0:2] 
    mask = np.zeros(imageSize, dtype=np.uint8)
    cv2.circle(mask,
               circleCenter, 
               circleRadius, 
               color=color, 
               thickness=-1)
    if returnMask:
        return mask
    return cv2.bitwise_and(img.astype(np.uint8), 
                           img.astype(np.uint8),
                           mask=mask.astype(np.uint8))