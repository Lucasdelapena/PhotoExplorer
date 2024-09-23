# Lucas de la Pena
# CS4420
# Assignment 2
# 9/23/2024

import cv2
import numpy as np
import random
import argparse

#selfnote: when getting pictures make sure to get copyright free and location of where you receieved the picture

def main():
    # Arguments
    parser = argparse.ArgumentParser(prog='browser') # -h should be automatically added because of argparse
    parser.add_argument('-a') # preserve the aspect ratio of the image
    parser.add_argument('-g') # save the output image as grayscale (default: save as input)
    parser.add_argument('-rows', type=int, default=0) # -r max number of rows
    parser.add_argument('-cols', type=int, default=0) # -c max number of cols
    parser.add_argument('indir') # input directory
    parser.add_argument('outdir') # output directory [default: indir.corpus]
    args = parser.parse_args()
    rows = args.rows
    cols = args.cols
    OrginRows = rows # made for dimensions
    OrginCols = cols

    

if __name__ == "__main__":
    main()