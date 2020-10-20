import numpy as np

from index.index import IndexIranGhazvin

from remotesensingmathematica.rs_mathematica import (
                                             RSMathematicaIranGhazvin,
)


class GhazvinBase(IndexIranGhazvin, RSMathematicaIranGhazvin):

    def __init__(self,
                 ndvi, nir, red, input_path,
                 wheat_minDay_peak_greenness=90,
                 wheat_maxday_peak_greenness=140,
                 wheat_minday_harvest=200,
                 wheat_maxday_harvest=300,
                 first_crop_peak_minday=150,
                 first_crop_peak_maxday=280,
                 second_crop_peak_minday=90,
                 second_crop_peak_maxday=280,
                 month_days=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                 month_days_leap=[31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                 T=0.2,
                 peak=2,
                 alfalfa_ndvi_threshold=0.2,
                 alfalfa_index_threshold=0.75,
                 alfalfa_radiance_coefficient=10000,
                 crop_mask_threshold=0.3,
                 maize_radiance_coefficient=10000,
                 maize_slope_threshold=150,
                 wheat_index_threshold=900,
                 ):

        self.ndvi = ndvi
        self.nir = nir
        self.red = red
        self.input_path = input_path
        self.month_days = month_days
        self.month_days_leap = month_days_leap
        self.T = T
        self.peak = peak
        self.crop_map = {
                            "season 1":
                            {
                              'alfalfa_index': 2,
                              'wheat_index_logic': 3,
                              'non_crop_pixels': 4,
                            },
                            "season 2":
                            {
                                "alfalfa_index": 2,
                                "maize_index": 3,
                                "non_crop_pixels": 4,
                            }
        }

        kwargs = {
                  'alfalfa_ndvi_threshold': alfalfa_ndvi_threshold,
                  'alfalfa_index_threshold': alfalfa_index_threshold,
                  'alfalfa_radiance_coefficient': alfalfa_radiance_coefficient,
                  'crop_mask_threshold': crop_mask_threshold,
                  'maize_radiance_coefficient': maize_radiance_coefficient,
                  'maize_slope_threshold': maize_slope_threshold,
                  'wheat_index_threshold': wheat_index_threshold,
        }

        super().__init__(**kwargs)

    def run(self, ):
        numfiles = self.num_files(self.input_path)
        # Extracting dates of files
        file_dates = self.file_names(self.input_path)

        # Conversion of Image dates,Sugarbeet_MinDay to julian days
        # using "JulianDay" function
        julianday = [int(self.julianday(i, self.month_days,
                         self.month_days_leap)) for i in file_dates]

        julianday = np.array(sorted(julianday))

        band_number_wheat_peak = julianday[np.logical_and(
                                 julianday > self.wheat_minDay_peak_greenness,
                                 julianday < self.wheat_maxday_peak_greenness
                                 )]

        band_number_wheat_harvest = julianday[
            np.logical_and(
                julianday > self.wheat_minday_harvest,
                julianday < self.wheat_maxday_harvest
            )]

        band_number_first_crop = julianday[
            np.logical_and(
                julianday > self.first_crop_peak_minday,
                julianday < self.first_crop_peak_maxday
            )]

        Band_Number_Second_Crop = julianday[
            np.logical_and(
                julianday > self.second_crop_peak_minday,
                julianday < self.second_crop_peak_maxday
            )]

        rank_julianday_peak = self.rank_julian_day(julianday,
                                                   band_number_wheat_peak)

        rank_julianday_harvest = self.rank_julian_day(julianday,
                                                      band_number_wheat_harvest)

        rank_julianday_s1 = self.rank_julian_day(julianday,
                                                 band_number_first_crop)

        rank_julianday_s2 = self.rank_julian_day(julianday,
                                                 Band_Number_Second_Crop)

        # Finding appropriate red bands for wheat index
        if len(rank_julianday_peak) == 1:
            Red_Peak = self.red[rank_julianday_peak]
        else:
            Red_Peak = self.red[
                        np.min(rank_julianday_peak):
                        np.max(rank_julianday_peak)+1
            ]

            Red_Peak = np.min(Red_Peak, axis=0)

        if len(rank_julianday_harvest) == 1:
            Red_Harvest = self.red[rank_julianday_harvest]
        else:
            Red_Harvest = self.red[
                            np.min(rank_julianday_harvest):
                            np.max(rank_julianday_harvest)+1
            ]

            Red_Harvest = np.max(Red_Harvest, axis=0)

        # Determination of maximum self.ndvi for first and second season
        if len(rank_julianday_s1) == 1:
            First_Season = self.ndvi[rank_julianday_s1]
        else:
            First_Season = self.ndvi[
                            np.min(rank_julianday_s1):
                            np.max(rank_julianday_s1)+1
            ]

        if len(rank_julianday_s2) == 1:
            Second_Season = self.ndvi[rank_julianday_s2]
        else:
            Second_Season = self.ndvi[
                            np.min(rank_julianday_s2):
                            np.max(rank_julianday_s2)+1
            ]

        Max_Second_Season = np.max(Second_Season, axis=0)

        # Crop mask (Separation of crops based on self.ndvi threshold)
        Crop_Mask = self.crop_mask(self.ndvi, numfiles)

        # a Predetermined 2D matrix with values of 1
        Previous_Classification_Image = np.ones_like(self.ndvi[0])

        # Detection of pixels with self.ndvi
        # in second season greater than 0.35
        Max_Second_Season_Logic = Max_Second_Season > 0.35

        # Calculation of alfalfa index for detecting alfalfa fields;
        alfalfa_index = self.alfalfa_index(
                            self.nir, self.red, self.ndvi,
                            rank_julianday_harvest, numfiles,
                            Previous_Classification_Image, Crop_Mask
        )

        Alfalfa_Index_Improved = self.find_peak(self.T, self.peak,
                                                alfalfa_index, self.ndvi)

        Previous_Classification_Image[Alfalfa_Index_Improved] = 0

        # Wheat index calculation using self.red
        # bands selected in appropriate dates
        wheat_index_logic = self.wheat_index(
                Red_Band_Greenness=Red_Peak,
                Red_Band_PostHarvest=Red_Harvest,
                Previous_Classification_Image=Previous_Classification_Image,
                Crop_Mask=Crop_Mask
        )

        # Detection of Maize
        maize_index = self.maize_index(
                                    self.ndvi,
                                    julianday,
                                    rank_julianday_s2,
                                    numfiles,
                                    Max_Second_Season,
                                    Max_Second_Season_Logic,
                                    Previous_Classification_Image
        )

        non_crop_pixels = np.logical_not(Crop_Mask)

        final_classification_image_s1 = np.ones_like(self.ndvi[0])
        final_classification_image_s2 = np.ones_like(self.ndvi[0])

        # Alfalfa
        final_classification_image_s1[alfalfa_index] = 2
        # Wheat and barley
        final_classification_image_s1[wheat_index_logic] = 3
        # Non crop
        final_classification_image_s1[non_crop_pixels] = 4
        # Alfalfa
        final_classification_image_s2[alfalfa_index] = 2
        # Maize
        final_classification_image_s2[maize_index] = 3
        # Non crop
        final_classification_image_s2[non_crop_pixels] = 4

        return {"final_classification_image_s1": final_classification_image_s1,
                "final_classification_image_s2": final_classification_image_s2,
                "crop_map": self.crop_map,
                }
