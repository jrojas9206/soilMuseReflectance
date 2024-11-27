import sys 
import argparse
from srmouse.ui.muse_ui import SimpleUI

def main():
    parser = argparse.ArgumentParser('SRMouse')
    parser.add_argument('path2spectralCube', type=str, help='Absoulute path to spectral cube')
    parser.add_argument('--scale', type=int, help='Scale use to resize the image for visualization. Default:4', default=4)
    parser.add_argument('--kernelSize', type=int, help='Kernel Size. Multiples of 2 are expected. Default: 2 2', nargs='+', default=[2,2])
    args = parser.parse_args()

    objSimpleUI = SimpleUI(args.path2spectralCube,
                           resizeScale=args.scale,
                           kernelSize=tuple(args.kernelSize))

    objSimpleUI.startUI()
    return 0 

if __name__ == '__main__':
    sys.exit(main())    
