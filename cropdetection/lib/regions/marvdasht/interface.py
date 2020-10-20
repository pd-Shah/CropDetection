import rasterio
import numpy as np

from django.conf import settings
from EastQazvin.src.CropDetection_EastQazvin.src.main import main

def run(NDVI, NIR, Red, InputPath, Wheat_MinDay_Peak_Greenness, Wheat_MaxDay_Peak_Greenness, Wheat_MinDay_Harvest, Wheat_MaxDay_Harvest, First_Crop_Peak_MinDay, First_Crop_Peak_MaxDay, Second_Crop_Peak_MinDay, Second_Crop_Peak_MaxDay, MonthDays, MonthDaysLeap, T, peak):
    print('alg is running')
    print('reading .tif files...')

    with rasterio.open(Red_path) as src:
        Red=src.read().astype(np.float)
        print(Red.shape)

    with rasterio.open(NIR_path) as src:
        NIR=src.read().astype(np.float)
        print(NIR.shape)

    with rasterio.open(NDVI_path) as src:
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


    Final_Classification_Image_S1, Final_Classification_Image_S2=main(NDVI,Red,NIR,InputPath,Wheat_MinDay_Peak_Greenness,Wheat_MaxDay_Peak_Greenness,Wheat_MinDay_Harvest,Wheat_MaxDay_Harvest,First_Crop_Peak_MinDay,First_Crop_Peak_MaxDay,Second_Crop_Peak_MinDay,Second_Crop_Peak_MaxDay,Sugarbeet_MinDay, MonthDays, MonthDaysLeap,T, peak)

    with rasterio.open(settings.MEDIA_ROOT+'/'+'EastQazvin/'+analysis_name+'/Overall_Classification_Image_S1.tif', 'w', driver='GTiff', height=Overall_Classification_Image_S1.shape[0],
                       width=Overall_Classification_Image_S1.shape[1], count=1, crs='+proj=latlong', dtype=rasterio.int32) as dst:
        dst.write(Overall_Classification_Image_S1, 1)

    with rasterio.open(settings.MEDIA_ROOT+'/'+'EastQazvin/'+analysis_name+'/Overall_Classification_Image_S2.tif', 'w', driver='GTiff', height=Overall_Classification_Image_S2.shape[0],
                       width=Overall_Classification_Image_S2.shape[1], count=1, crs='+proj=latlong', dtype=rasterio.int32) as dst:
        dst.write(Overall_Classification_Image_S2, 1)

    return str('EastQazvin/'+analysis_name+'/Overall_Classification_Image_S1.tif'), str('EastQazvin/'+analysis_name+'/Overall_Classification_Image_S2.tif')

    InputPath='/home/aras/Documents/Marvdasht/Marvdasht/Sentinel'

    Final_Classification_Image_S1, Final_Classification_Image_S2=main(NDVI, NIR, Red, InputPath, Wheat_MinDay_Peak_Greenness, Wheat_MaxDay_Peak_Greenness, Wheat_MinDay_Harvest, Wheat_MaxDay_Harvest, First_Crop_Peak_MinDay, First_Crop_Peak_MaxDay, Second_Crop_Peak_MinDay, Second_Crop_Peak_MaxDay, MonthDays, MonthDaysLeap, T, peak)
