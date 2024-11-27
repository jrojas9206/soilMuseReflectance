import os 
import cv2
import numpy as np 
from pathlib import Path
from matplotlib import pyplot as plt 
from srmouse.viz import showManualPoint 
class SimpleUI:
    '''
        UI to visualize in a fast way the Spectral Cube of Digital Number [DN]
    '''

    EXPECTED_BANDS = [365, 400, 465, 540, 640, 700, 750, 800, 850, 900, 950, 1000]
    UI_NAME = 'SRMOUSE'

    def __init__(self, path2image:str, resizeScale:int=4, kernelSize:tuple=(2,2), imageExtension:str='jpg', crossSize:int=10, crossThickness:int=2):
        '''
            Contructor

            Parameters
            -----------
                path2image : str, Absolute path to directory that contain the image set. The image on the
                                  folder must have the name with the following format imageBAND.jpg. Where BAND
                                  is a integer in the list of accepted bands.
                resizeScale : int, Integer number that will be use to re-scale the image. Multiples of 2 are expected. Default 4 
                kernelSize : tuple, Size of the kernel used to extract the pixels. Default (2,2)
                imageExtension : str, Extension of the images to load. Default: 'jpg'
        '''
        self._path2image = str(Path(path2image).resolve())
        self._scale = resizeScale
        self._kernelSize = kernelSize
        self._dictDN = {band:[] for band in self.EXPECTED_BANDS}
        self._pointCoordinates = [] # [[x0,y0], [x1,y1], ..., [xn,yn]]
        self._multispectralImage = np.array([])
        self._image2show = np.array([])
        self._imageExtension = imageExtension
        self._signatures = []
        self._crossSize = crossSize
        self._crossThickness = crossThickness
        self.fig, self.ax = plt.subplots()
        self.ax.set_xticks(range(1, len(self.EXPECTED_BANDS)+1), self.EXPECTED_BANDS)
        self.ax.set_title('Multispectral Siganture')
        self.ax.set_xlabel('Band(pixels)')
        self.ax.set_ylabel('Intensity')
        self.fig.canvas.manager.set_window_title(self.UI_NAME) 
        self.fig.tight_layout()
        if self._scale%2 != 0:
            raise ValueError('The scale must be a multiple of 2 and got %i' %(self._scale))
        self._loadAndPrepareImage()

    def _loadAndPrepareImage(self) -> None:
        '''
            Load the jpg images that represent each of the 12 bands
            captured by the MUSE Multispectral camera and create a fake 
            color image to for visualization purposes.
        '''
        for index, cBand in enumerate(self.EXPECTED_BANDS):
            imageName = f'image{cBand}.{self._imageExtension}'
            path2image = os.path.join(self._path2image, imageName)
            imageArray = cv2.imread(path2image, cv2.IMREAD_GRAYSCALE) 
            if index == 0:
                self._multispectralImage = imageArray
            else:
                self._multispectralImage = np.dstack([self._multispectralImage, imageArray])
        self._image2show = self._multispectralImage[:,:,0:3] # Create an image with the first 3 bands and rescaled
        self._image2show = cv2.resize(self._image2show, 
                                      (int(self._image2show.shape[1]/self._scale), int(self._image2show.shape[0]/self._scale)))

    def __click_event(self, event, x, y, flags, params):
        '''
            Catch the events that occur in the CV2 Ui interface 

            See the OPENCV documentation for more detail information 
        '''
        halfPosKernelX, halfPosKernelY = int(self._kernelSize[0]/2), int(self._kernelSize[1]/2) 
        if event == cv2.EVENT_LBUTTONDOWN:
            listLegends = []
            self._pointCoordinates.append([int(x*self._scale), int(y*self._scale)])
            cropImage = self._multispectralImage[x-halfPosKernelX:x+halfPosKernelX, y-halfPosKernelY:y+halfPosKernelX, :]
            meanValuesPerBand = self.getValuesFromMultispectralImage(cropImage)
            self._signatures.append(meanValuesPerBand)
            self._image2show = showManualPoint(self._image2show,
                                               [[x,y]],
                                               cross=self._crossSize,
                                               thikness=self._crossThickness,
                                               returnImage=True)
            cv2.imshow(self.UI_NAME, self._image2show)
            for indexSignatures, signature in enumerate(self._signatures, start=1):
                self.ax.plot(range(1,13), signature)
                listLegends.append(f'Point: {indexSignatures}')
            self.ax.set_xticks(range(1, len(self.EXPECTED_BANDS)+1), self.EXPECTED_BANDS)
            self.ax.set_title('Multispectral Siganture')
            self.ax.set_xlabel('Band(pixels)')
            self.ax.set_ylabel('Intensity')
            self.ax.legend(listLegends)
            self.fig.canvas.manager.set_window_title(self.UI_NAME) 
            self.fig.tight_layout()
            plt.draw()

    def getValuesFromMultispectralImage(self, cropImage:np.array) -> list:
        '''
            Get the avarange value from the croped image 

            Paramters
            ---------

                    cropImage : numpy.array, Numpy array of size (N,M,12)
            
            Return 
            ------
                list 

            NOTE
            ----
                The values of the returned image are in the same order as the ones of the 
                EXPECTED_BANDS
        '''
        lst2return = []
        for bandIndex in range(len(self.EXPECTED_BANDS)):
            averageValue = np.mean(cropImage[:, :, bandIndex])
            lst2return.append(averageValue)
        return lst2return
    
    def startUI(self):
        cv2.imshow(self.UI_NAME, self._image2show)
        cv2.setMouseCallback(self.UI_NAME, 
                             self.__click_event)
        plt.show()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
