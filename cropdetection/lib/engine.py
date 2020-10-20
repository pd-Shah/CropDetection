from matplotlib import pyplot as plt
import numpy as np
import rasterio
import importlib
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from cropdetection import models
from .regions.marvdasht.src import main

def connect_engine(pk):

    analyze = get_object_or_404(models.Analyze, pk=pk)

    # dynamic load package
    lib_dir = analyze.region.name.split('_')
    class_name = lib_dir[-1].title()
    class_dir = 'cropdetection.lib.region.' + '.'.join(lib_dir) + '.' + lib_dir[-1]
    module = importlib.import_module(class_dir)
    klass = getattr(module, class_name)

    if not analyze.result:
        red_path = analyze.get_red_path()
        ndvi_path = analyze.get_ndvi_path()
        near_infrared_path = analyze.get_nir_path()
        input_path = analyze.get_inputpath_path()

        print("reading files...")
        with rasterio.open(red_path) as src:
            red = src.read().astype(np.float)

        with rasterio.open(ndvi_path) as src:
            ndvi = src.read().astype(np.float)

        with rasterio.open(near_infrared_path) as src:
            nir = src.read().astype(np.float)
        print('done!')

        obj = klass(ndvi=ndvi,
                    nir=nir,
                    red=red,
                    input_path=input_path,)

        result = getattr(obj, 'run')()

        crop_map = result['crop_map']

        if 'final_classification_image_s2' in result:
            result = (
                      result['final_classification_image_s1'],
                      result['final_classification_image_s2']
            )

            path = '{0}/CropDetectionApp/Regions/{1}/Analyzes/{2}/result_1.jpg'.format(
                           settings.MEDIA_ROOT, analyze.region.name, analyze.id
                  )

            plt.imsave(path, result['final_classification_image_s1'])

            path = '{0}/CropDetectionApp/Regions/{1}/Analyzes/{2}/result_2.jpg'.format(
                           settings.MEDIA_ROOT, analyze.region.name, analyze.id
                  )

            plt.imsave(path, result['final_classification_image_s2'])

            path = 'CropDetectionApp/Regions/{0}/Analyzes/{1}/result_1.jpg'.format(
                           analyze.region.name, analyze.id
                  )
            analyze.result_image_1 = path

            path = 'CropDetectionApp/Regions/{0}/Analyzes/{1}/result_2.jpg'.format(
                           analyze.region.name, analyze.id
                  )
            analyze.result_image_2 = path

        else:
            result = result['final_classification_image_s1']

            path = '{0}/CropDetectionApp/Regions/{1}/Analyzes/{2}/result_1.jpg'.format(
                           settings.MEDIA_ROOT, analyze.region.name, analyze.id
                  )

            plt.imsave(path, result['final_classification_image_s1'])

            path = 'CropDetectionApp/Regions/{0}/Analyzes/{1}/result_1.jpg'.format(
                           analyze.region.name, analyze.id
                  )
            analyze.result_image_1 = path

        if len(result) == 2:
            result = np.dstack(result)
            result = np.rollaxis(result, -1)

        else:
            result = result.reshape((1, result.shape[0], result.shape[1]))

        path = '{0}/CropDetectionApp/Regions/{1}/Analyzes/{2}/result.tif'.format(
                       settings.MEDIA_ROOT, analyze.region.name, analyze.id
              )

        with rasterio.open(path, 'w', driver='GTiff',
                           height=result.shape[1],
                           width=result.shape[2],
                           count=result.shape[0],
                           crs='+proj=latlong',
                           dtype=rasterio.int32) as dst:
            dst.write(result.astype(np.int32))

        path = 'CropDetectionApp/Regions/{0}/Analyzes/{1}/result.tif'.format(
                       analyze.region.name, analyze.id
              )
        analyze.result = path

        analyze.color_map = crop_map
        analyze.save()
        return analyze

    elif analyze.result:
            return analyze
def marvdasht(pk):
    print("dsa"*100)
    object_=get_object_or_404(models.Analyze, pk=pk)

    red=object_.get_red_path()
    ndvi=object_.get_ndvi_path()
    NIR=object_.get_nir_path()
    with rasterio.open(red) as src:
        red = src.read().astype(np.float)
    with rasterio.open(ndvi) as src:
        ndvi = src.read().astype(np.float)
    with rasterio.open(NIR) as src:
        NIR = src.read().astype(np.float)
    inputpath=object_.get_inputpath_path()
    # InputPath='/home/aras/Documents/Marvdasht/Marvdasht/Sentinel'
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

    final_classification_image_s1, final_classification_image_s2 =main.main(NDVI, NIR, Red, InputPath, Wheat_MinDay_Peak_Greenness, Wheat_MaxDay_Peak_Greenness, Wheat_MinDay_Harvest, Wheat_MaxDay_Harvest, First_Crop_Peak_MinDay, First_Crop_Peak_MaxDay, Second_Crop_Peak_MinDay, Second_Crop_Peak_MaxDay, MonthDays, MonthDaysLeap, T, peak)

    path = '{0}/CropDetectionApp/Regions/{1}/Analyzes/{2}/result_1.jpg'.format(
                           settings.MEDIA_ROOT, object_.region.name, object_.id
                  )
    plt.imsave(path, final_classification_image_s1)
    path='CropDetectionApp/Regions/{0}/Analyzes/{1}/result_1.jpg'.format(
                            object_.region.name, object_.id
                  )
    object_.result_image_1=path
    path = '{0}/CropDetectionApp/Regions/{1}/Analyzes/{2}/result_2.jpg'.format(
                           settings.MEDIA_ROOT, object_.region.name, object_.id
                  )
    plt.imsave(path, final_classification_image_s2)
    path = 'CropDetectionApp/Regions/{0}/Analyzes/{1}/result_2.jpg'.format(
        object_.region.name, object_.id
            )
    
    object_.result_image_2=path
    object_.save()
