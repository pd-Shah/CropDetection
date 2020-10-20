import numpy as np

from cropdetection.lib.index.index import IndexIranKhorasanRazavi
from cropdetection.lib.remotesensingmathematica.rs_mathematica import DayFilePeak


class KhorasanRazaviBase(IndexIranKhorasanRazavi, DayFilePeak):

    def __init__(self,
                 ndvi,
                 nir,
                 red,
                 input_path,
                 wheat_minday_peak_greenness=90,
                 wheat_maxday_peak_greenness=140,
                 wheat_minday_harvest=160,
                 wheat_maxday_harvest=210,
                 first_crop_peak_minmay=90,
                 first_crop_peak_maxday=140,
                 second_crop_peak_minday=160,
                 second_crop_peak_maxday=350,
                 T=0.15,
                 peak=2,
                 month_days=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                 month_days_leap=[31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                 alfalfa_index_threshold=0.75,
                 alfalfa_radiance_coefficient=10000,
                 alfalfa_ndvi_threshold=0.2,
                 wheat_index_threshold=600,
                 maize_radiance_coefficient=10000,
                 maize_slope_threshold=150,
                 maize_growth_period_threshold=140,
                 crop_mask_ndvi_threshold=0.3
                 ):

        self.ndvi = ndvi
        self.nir = nir
        self.red = red
        self.input_path = input_path
        self.month_days = month_days
        self.month_days_leap = month_days_leap
        self.T = T
        self.peak = peak
        self.wheat_minday_peak_greenness = wheat_minday_peak_greenness
        self.wheat_maxday_peak_greenness = wheat_maxday_peak_greenness
        self.wheat_minday_harvest = wheat_minday_harvest
        self.wheat_maxday_harvest = wheat_maxday_harvest
        self.first_crop_peak_minday = first_crop_peak_minmay
        self.first_crop_peak_maxday = first_crop_peak_maxday
        self.second_crop_peak_minday = second_crop_peak_minday
        self.second_crop_peak_maxday = second_crop_peak_maxday
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
                  'maize_radiance_coefficient': maize_radiance_coefficient,
                  'maize_slope_threshold': maize_slope_threshold,
                  'wheat_index_threshold': wheat_index_threshold,
                  'maize_growth_period_threshold': maize_growth_period_threshold,
                  'crop_mask_ndvi_threshold': crop_mask_ndvi_threshold,
        }

        super().__init__(**kwargs)

    def run(self, ):

        # Counting number of files
        numfiles = self.num_files(self.input_path)
        # Extracting dates of files
        file_dates = self.file_names(self.input_path)

        # Conversion of Image dates,Sugarbeet_MinDay to julian days
        # using "JulianDay" function
        julianday = [int(self.julianday(i, self.month_days,
                         self.month_days_leap)) for i in file_dates]

        julianday = np.array(sorted(julianday))

        band_number_wheat_peak = julianday[np.logical_and(
                                 julianday > self.wheat_minday_peak_greenness,
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

        band_number_second_crop = julianday[
            np.logical_and(
                julianday > self.second_crop_peak_minday,
                julianday < self.second_crop_peak_maxday
            )]

        rank_julianday_peak = self.rank_julian_day(julianday,
                                                   band_number_wheat_peak)

        rank_julianday_harvest = self.rank_julian_day(
                                                      julianday,
                                                      band_number_wheat_harvest
        )

        rank_julianday_s1 = self.rank_julian_day(julianday,
                                                 band_number_first_crop)

        rank_julianday_s2 = self.rank_julian_day(julianday,
                                                 band_number_second_crop)

        # Finding appropriate red bands for wheat index
        if len(rank_julianday_peak) == 1:
            red_peak = self.red[rank_julianday_peak]
        else:
            red_peak = self.red[
                                np.min(rank_julianday_peak):
                                np.max(rank_julianday_peak)+1
            ]
            red_peak = np.min(red_peak, axis=0)

        if len(rank_julianday_harvest) == 1:

            red_harvest = self.red[rank_julianday_harvest]
            red_harvest = red_harvest[0]
        else:
            red_harvest = self.red[
                                    np.min(rank_julianday_harvest):
                                    np.max(rank_julianday_harvest)+1
            ]
            red_harvest = np.max(red_harvest, axis=0)

        # Determination of maximum self.ndvi for first and second season
        if len(rank_julianday_s1) == 1:
            first_season = self.ndvi[rank_julianday_s1]
        else:
            first_season = self.ndvi[
                                    np.min(rank_julianday_s1):
                                    np.max(rank_julianday_s1)+1
            ]

        if len(rank_julianday_s2) == 1:
            second_season = self.ndvi[rank_julianday_s2]
        else:
            second_season = self.ndvi[
                                        np.min(rank_julianday_s2):
                                        np.max(rank_julianday_s2)+1
            ]

        max_second_season = np.max(second_season, axis=0)

        # Crop mask (Separation of crops based on self.ndvi threshold)
        crop_mask = self.crop_mask(self.ndvi, numfiles)

        # a Predetermined 2D matrix with values of 1
        Previous_Classification_Image = np.ones_like(
                                                    self.ndvi[0],
                                                    dtype=np.bool
        )

        # Detection of pixels with self.ndvi in second season greater than 0.35
        Max_Second_Season_Logic = max_second_season > 0.35

        # Calculation of alfalfa index for detecting alfalfa fields;
        Alfalfa_Index = self.alfalfa_index(
                                        self.nir,
                                        self.red,
                                        self.ndvi,
                                        rank_julianday_harvest,
                                        numfiles,
                                        Previous_Classification_Image,
                                        crop_mask,
        )

        Alfalfa_Index_Improved = self.find_peak(
                                                self.T,
                                                self.peak,
                                                Alfalfa_Index,
                                                self.ndvi
        )

        Previous_Classification_Image[
                                    Alfalfa_Index_Improved.astype(np.bool)
        ] = 0

        # Wheat index calculation using self.red
        # bands selected in appropriate dates
        Wheat_Index_logic = self.wheat_index(
                                             red_peak,
                                             red_harvest,
                                             Previous_Classification_Image,
                                             crop_mask=1,
                                             max_second_season_logic=0,
                                             mask_wheat=1,
        )

        Previous_Classification_Image[Wheat_Index_logic.astype(np.bool)] = 0

        # Detection of Maize
        Maize_Index = self.maize_index(
                                       self.ndvi,
                                       julianday,
                                       rank_julianday_s2, numfiles,
                                       max_second_season,
                                       Max_Second_Season_Logic,
                                       Previous_Classification_Image
        )

        Previous_Classification_Image[Maize_Index.astype(np.bool)] = 0

        Non_Crop_Pixels = np.logical_not(crop_mask.astype(np.bool))

        final_classification_image_s1 = np.ones_like(self.ndvi[0])
        final_classification_image_s2 = np.ones_like(self.ndvi[0])

        # Alfalfa
        final_classification_image_s1[
                                    Alfalfa_Index_Improved.astype(np.bool)
        ] = 2

        # Wheat and barley
        final_classification_image_s1[Wheat_Index_logic.astype(np.bool)] = 3

        # Non crop
        final_classification_image_s1[Non_Crop_Pixels.astype(np.bool)] = 4

        # Alfalfa
        final_classification_image_s2[
                                      Alfalfa_Index_Improved.astype(np.bool)
        ] = 2

        # Maize
        final_classification_image_s2[Maize_Index.astype(np.bool)] = 3

        # Non crop
        final_classification_image_s2[Non_Crop_Pixels.astype(np.bool)] = 4

        return {"final_classification_image_s1":
                final_classification_image_s1,
                "final_classification_image_s2":
                final_classification_image_s2,
                "crop_map": self.crop_map,
                }
