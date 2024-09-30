# Lucas de la Pena
# CS4420
# Assignment 2
# 9/23/2024

import cv2
import numpy as np
import random
import os
import argparse
#from PIL import Image // i dont know what this is used for
from screeninfo import get_monitors

#selfnote: when getting pictures make sure to get copyright free and location of where you receieved the picture

def main():
    # Arguments
    parser = argparse.ArgumentParser(prog='corpus') # -h should be automatically added because of argparse
    parser.add_argument('-a', action='store_true') # preserve the aspect ratio of the image
    parser.add_argument('-g', action='store_true') # save the output image as grayscale (default: save as input)
    parser.add_argument('-rows', type=int, default=480) # -r max number of rows
    parser.add_argument('-cols', type=int, default=640) # -c max number of cols
    parser.add_argument('-t') #output image type (jpg, tif, bmp, or png)
    parser.add_argument('indir') # input directory
    parser.add_argument('outdir')#, default=indir.corpus # output directory [default: indir.corpus]
    args = parser.parse_args()
    a = args.a
    g = args.g
    rows = args.rows
    cols = args.cols
    t = args.t
    indir = args.indir
    outdir = args.outdir
    OrginRows = rows # made for dimensions
    OrginCols = cols

    print("a: ", a)
    print("g: ", g)
    print("rows: ", rows)
    print("cols: ", cols)
    print("t: ", t)
    print("indir: ", indir)
    print("outdir: ", outdir)

    #checking for valid input -t type
    if t != None:
        if t != "jpg" and t != "tif" and t != "bmp" and t != "png":
            print("Invalid output image type. Please use jpg, tif, bmp, or png")
            exit()
        outputType = t

    # Get monitor information
    for m in get_monitors(): #note: this gets takes the last monitor info
        maxWidth = m.width
        maxHeight = m.height
    
    # Create output directory
    if outdir == None:
        outdir = indir + ".corpus"
        os.makedirs(outdir, exist_ok=True)
    else:
        os.makedirs(outdir, exist_ok=True)

     # Check if rows and cols are greater than the monitor size
    if rows > maxWidth:
        rows = maxWidth - 200
    if cols > maxHeight:
        cols = maxHeight - 200

    # lists and directory
    dir = args.indir
    picslist = []
    filenameList = []

    # gets directory path, directory names, and file names
    for dirpath, dirnames, filenames in os.walk(dir, topdown=False): 
        for filename in filenames:
            picslist.append(os.path.join(dirpath, filename))
            filenameList.append(filename)

    # This is for no window resizing
    if rows == 0 or cols == 0:
        noWinChange = True
    else:
        noWinChange = False
        cv2.namedWindow("Image Window", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Image Window', rows, cols)

    imageNumber = 0 # counter for loop
    while True:
        pic = picslist[imageNumber]
        # Read the image
        image = cv2.imread(pic)

        # Check if the image was successfully loaded
        if image is None:
            filenameList.pop(imageNumber) # removing non-image files from the list
            picslist.pop(imageNumber)
            continue

        # No window resizing
        if noWinChange == True: #This works
            cv2.imshow('Image Window', image)
            
            #This is for if the image is bigger than the screen
            if image.shape[1] > maxWidth or image.shape[0] > maxHeight:
               
                width = image.shape[1]
                height = image.shape[0]
                ratio = width / height

                if width > maxWidth:
                    newWidth = maxWidth - 200
                    newHeight = int(newWidth / ratio)
                elif height > maxHeight:
                    newHeight = maxHeight - 200
                    newWidth = int(newHeight * ratio)
                else:
                    newWidth = width
                    newHeight = height
            else:
                newWidth = image.shape[1]
                newHeight = image.shape[0]        

            image = cv2.resize(image, (newWidth, newHeight ))
            cv2.resizeWindow('Image Window', newWidth , newHeight)
            cv2.imshow('Image Window', image)
           
        #Window resizing
        else: #here change it so if the image is bigger than max rows and cols change it
            if image.shape[1] > OrginCols or image.shape[0] > OrginRows:
                width = image.shape[1]
                height = image.shape[0]
                ratio = width / height

                if width > OrginCols:
                    newWidth = OrginCols
                    newHeight = int(newWidth / ratio)
                elif height > OrginRows:
                    newHeight = OrginRows
                    newWidth = int(newHeight * ratio)
                else:
                    newWidth = width
                    newHeight = height
            
            #newWidth = OrginRows
            #newHeight = OrginCols
            cv2.imshow('Image Window', image)

        # Grayscale
        if g == True:
            outputPath = os.path.join(outdir, filenameList[imageNumber])
            if os.path.exists(outputPath):
                continue
            else:
                # convert to typ
                imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(f"{outdir}/{filenameList[imageNumber]}.{t}", imageGray)

        # Output Variables
        fileName = filenameList[imageNumber]
        filePath = os.path.dirname(pic)
        imageDimensions = f"{newWidth} x {newHeight}"
        numOfPixels = image.size
        fileSize = os.path.getsize(pic)
        fileType = os.path.splitext(pic)[1]

        # Display value at a random pixel
        rows, cols, _ = image.shape
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        pixelColor = image[r, c]
        colorPixel = f"({int(pixelColor[0])}, {int(pixelColor[1])}, {int(pixelColor[2])})"

        #outputs
        print(f"File name: {fileName} | File path: {filePath} | Dimensions: {imageDimensions} | "
            f"Pixel Count: {numOfPixels} | File size: {fileSize} bytes | File type: {fileType} | "
            f"Color pixel at ({r},{c}) = {colorPixel}")

        #writing outputs to a file
        with open(f"metadata", "a") as file:
            file.write(f"File name: {fileName} | File path: {filePath} | Dimensions: {imageDimensions} | "
            f"Pixel Count: {numOfPixels} | File size: {fileSize} bytes | File type: {fileType} | "
            f"Color pixel at ({r},{c}) = {colorPixel}\n")

        # User actions
        useraction = cv2.waitKey(0) & 0xFF
    
        if useraction == ord('n'):
            if imageNumber < len(picslist) - 1:
                imageNumber += 1
        
        if useraction == ord('p'):
            if imageNumber > 0:
                imageNumber -= 1

        if useraction == ord('q'):
            break

    

if __name__ == "__main__":
    main()