import sys 
import argparse 
from matplotlib import pyplot as plt
from srmouse.processor import LoadMeasurements
from srmouse.viz import plotReflectanceSignatures

def fastPlot(ARGS):
    path_to_folder = ARGS.path2data  # Write here the full path to folder with your data acquired with MUSES9 multispectral camera

    path2measurements = ARGS.output

    lstValues, lstNames = LoadMeasurements(path_to_folder)

    plotReflectanceSignatures(lstValues, 
                            idx2skip=0, 
                            avgPlot=True, 
                            filesNames=lstNames)

    plt.savefig(path2measurements, dpi=150)

def main():
    parser = argparse.ArgumentParser('CMD to save the reflectance signature')
    parser.add_argument('path2data', type=str, help='Path to the measurements done with the Muses9 Camera')
    parser.add_argument('output', type=str, help='Name of the outputfile')
    parser.add_argument('--dpi', type=int, help='Plot resolution. Default 150', default=150)
    parser.add_argument('--noAvgPlot', help='If true all the plots will be shown', action='store_false')
    args = parser.parse_args()
    fastPlot(args)
    return 0

if __name__ == '__main__':
    sys.exit(main())