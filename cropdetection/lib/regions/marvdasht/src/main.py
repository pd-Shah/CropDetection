# from . import rs_mathematica as rs
from . import rs_mathmatica as rs
import numpy as np
from matplotlib import pyplot as plt
import rasterio
import glob
import os

def main(NDVI, NIR, Red, InputPath, Wheat_MinDay_Peak_Greenness, Wheat_MaxDay_Peak_Greenness, Wheat_MinDay_Harvest, Wheat_MaxDay_Harvest, First_Crop_Peak_MinDay, First_Crop_Peak_MaxDay, Second_Crop_Peak_MinDay, Second_Crop_Peak_MaxDay, MonthDays, MonthDaysLeap, T, peak):
    '''
    season 1:
    Alfalfa_Index = 2
    Wheat_Index_logic = 3
    Non_Crop_Pixels = 4

    season 2:
    Alfalfa_Index = 2
    Maize_Index = 3
    Non_Crop_Pixels = 4
    '''
    # Counting number of files and dates of them from input folder determined by user above
    #Counting number of files
    numfiles=rs.NumFiles(InputPath)

    #Extracting dates of files
    FileDates=rs.FileNames(InputPath)

    # Conversion of Image dates,Sugarbeet_MinDay to julian days using "JulianDay" function
    julianday=[int(rs.julianday(i, MonthDays, MonthDaysLeap)) for i in FileDates]
    julianday=np.array(sorted(julianday))

    Band_Number_Wheat_Peak=julianday[np.logical_and(julianday>Wheat_MinDay_Peak_Greenness, julianday<Wheat_MaxDay_Peak_Greenness)]
    Band_Number_Wheat_Harvest=julianday[np.logical_and(julianday>Wheat_MinDay_Harvest,julianday<Wheat_MaxDay_Harvest)]
    Band_Number_First_Crop=julianday[np.logical_and(julianday>First_Crop_Peak_MinDay,julianday<First_Crop_Peak_MaxDay)]
    Band_Number_Second_Crop=julianday[np.logical_and(julianday>Second_Crop_Peak_MinDay,julianday<Second_Crop_Peak_MaxDay)]

    Rank_JulianDay_Peak=rs.RankJulianDay(julianday,Band_Number_Wheat_Peak)
    Rank_JulianDay_Harvest=rs.RankJulianDay(julianday,Band_Number_Wheat_Harvest)
    Rank_JulianDay_S1=rs.RankJulianDay(julianday,Band_Number_First_Crop)
    Rank_JulianDay_S2=rs.RankJulianDay(julianday,Band_Number_Second_Crop)

    # Finding appropriate red bands for wheat index
    if len(Rank_JulianDay_Peak)==1:
        Red_Peak=Red[Rank_JulianDay_Peak][0]

    else :
        Red_Peak=Red[np.min(Rank_JulianDay_Peak): np.max(Rank_JulianDay_Peak)+1]
        Red_Peak=np.min(Red_Peak, axis=0)

    if len(Rank_JulianDay_Harvest)==1:
        Red_Harvest=Red[Rank_JulianDay_Harvest]
    else:
        Red_Harvest=Red[np.min(Rank_JulianDay_Harvest):np.max(Rank_JulianDay_Harvest)+1]
        Red_Harvest=np.max(Red_Harvest, axis=0)

    #  Determination of maximum NDVI for first and second season
    if len(Rank_JulianDay_S1)==1:
        First_Season=NDVI[Rank_JulianDay_S1]
    else:
        First_Season=NDVI[np.min(Rank_JulianDay_S1):np.max(Rank_JulianDay_S1)+1]

    Max_First_Season=np.max(First_Season, axis=0)

    if len(Rank_JulianDay_S2)==1:
        Second_Season=NDVI[Rank_JulianDay_S2]
    else:
        Second_Season=NDVI[np.min(Rank_JulianDay_S2):np.max(Rank_JulianDay_S2)+1]

    Max_Second_Season=np.max(Second_Season,axis=0)
    Min_Second_Season=np.min(Second_Season,axis=0)

    # Crop mask (Separation of crops based on NDVI threshold)
    Crop_Mask=rs.CropMask(NDVI,numfiles)

    # a Predetermined 2D matrix with values of 1
    Previous_Classification_Image=np.ones_like(NDVI[0])

    # Detection of pixels with NDVI in second season greater than 0.35
    Max_Second_Season_Logic=Max_Second_Season>0.35

    #Calculation of alfalfa index for detecting alfalfa fields;
    Alfalfa_Index= rs.Build_Alfalfa_Index( NIR, Red, NDVI, Rank_JulianDay_Harvest, numfiles, Previous_Classification_Image, Crop_Mask )

    Alfalfa_Index_Improved = rs.Find_Peak(T, peak, Alfalfa_Index,NDVI)
    Previous_Classification_Image [Alfalfa_Index_Improved] = 0

    #Wheat index calculation using Red bands selected in appropriate dates
    Wheat_Index_logic = rs.Build_Wheat_Index(Red_Peak, Red_Harvest, Previous_Classification_Image)

    #Detection of Maize
    Maize_Index = rs.Build_Maize_Index(NDVI,  julianday, Rank_JulianDay_S2, numfiles, Max_Second_Season, Max_Second_Season_Logic, Previous_Classification_Image)

    Non_Crop_Pixels = np.logical_not(Crop_Mask)

    Final_Classification_Image_S1= np.ones_like(NDVI[0])
    Final_Classification_Image_S2= np.ones_like(NDVI[0])

    #Alfalfa
    Final_Classification_Image_S1 [Alfalfa_Index] = 2
    #Wheat and barley
    Final_Classification_Image_S1 [Wheat_Index_logic] = 3
    #Non crop
    Final_Classification_Image_S1 [Non_Crop_Pixels] = 4
    #Alfalfa
    Final_Classification_Image_S2 [Alfalfa_Index] = 2
    #Maize
    Final_Classification_Image_S2 [Maize_Index] = 3
    #Non crop
    Final_Classification_Image_S2 [Non_Crop_Pixels] = 4

    return Final_Classification_Image_S1, Final_Classification_Image_S2

if __name__ == '__main__' :

    with rasterio.open("/home/aras/Documents/Marvdasht/Segments/Red_Composite_Marvdasht_SW.tif") as src:
        Red=src.read().astype(np.float)
        print(Red.shape)

    with rasterio.open("/home/aras/Documents/Marvdasht/Segments/NIR_Composite_Marvdasht_SW.tif") as src:
        NIR=src.read().astype(np.float)
        print(NIR.shape)

    with rasterio.open("/home/aras/Documents/Marvdasht/Segments/NDVI_Composite_Marvdasht_SW.tif") as src:
        NDVI=src.read().astype(np.float)
        print(NDVI.shape)

    Wheat_MinDay_Peak_Greenness = 90
    Wheat_MaxDay_Peak_Greenness = 140
    Wheat_MinDay_Harvest =        200
    Wheat_MaxDay_Harvest =        300
    First_Crop_Peak_MinDay=       150
    First_Crop_Peak_MaxDay =      280
    Second_Crop_Peak_MinDay =     90
    Second_Crop_Peak_MaxDay =     280

    T=0.14
    peak=3

    #number of days in each month (Gregorian Calendar) in a nonleap year
    MonthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
    #number of days in each month (Gregorian Calendar) in a leap year
    MonthDaysLeap = [31,29,31,30,31,30,31,31,30,31,30,31]

    InputPath='/home/aras/Documents/Marvdasht/Marvdasht/Sentinel'

    Final_Classification_Image_S1, Final_Classification_Image_S2=main(NDVI, NIR, Red, InputPath, Wheat_MinDay_Peak_Greenness, Wheat_MaxDay_Peak_Greenness, Wheat_MinDay_Harvest, Wheat_MaxDay_Harvest, First_Crop_Peak_MinDay, First_Crop_Peak_MaxDay, Second_Crop_Peak_MinDay, Second_Crop_Peak_MaxDay, MonthDays, MonthDaysLeap, T, peak)

    plt.imshow(Final_Classification_Image_S1)
    plt.show()

    plt.imshow(Final_Classification_Image_S2)
    plt.show()
