import numpy as np

from ..base import ArdebilBase


class Ardebil(ArdebilBase):

    def __init__(self, **kwargs):
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

        # Crop mask (Separation of crops based on self.ndvi threshold)
        Crop_Mask = self.crop_mask(self.ndvi, numfiles)
        # Detecting non crop pixels
        non_crop_pixels = np.logical_not(Crop_Mask)

        # a Predetermined 2D matrix with values of 1
        Previous_Classification_Image = np.ones_like(self.ndvi[0])

        Max_Second_Season = np.max(Second_Season, axis=0)

        # NIR peak calculation
        Max_NIR = np.max(self.nir, axis=0)

        # Rank of NIR peak layer
        Max_Day_Rank = self.Find_MaxDay(self.nir, Max_NIR)

        # Assignment of rank to pixels with slope in potato season
        Max_Potato = self.Find_Max(Max_Day_Rank)

        # Find Red band value for band corresponding to NIR peak
        Min_Red = self.Find_Min(Max_Day_Rank, self.red)

        # Find minimum of NIR in potato harvest time
        NIR_Harvest = self.nir[9:numfiles+1]
        NIR_Harvest = np.min(NIR_Harvest, axis=0)

        # Slope from start of season to NIR peak time
        Slope = self.Find_Slope(Max_Day_Rank, self.nir)

        # Find minimum of NIR in cultivated time
        NIR_Cultivation = self.nir[2]

        # Calculate NIR_MIN of harvest and cultivation time
        NIR_MIN = (1.0/(NIR_Harvest+NIR_Cultivation))

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
        )

        Previous_Classification_Image[wheat_index_logic] = 0

        # # Calculation of Potato_Index
        # potato_classification_image = self.potato_index(
        #                              self.ndvi, Slope,
        #                              Max_NIR, Min_Red, NIR_Harvest,
        #                              NIR_MIN, Previous_Classification_Image
        # )

        final_classification_image_s1 = np.ones_like(self.ndvi[0])
        final_classification_image_s2 = np.ones_like(self.ndvi[0])

        # Alfalfa
        final_classification_image_s1[alfalfa_index] = 2
        # Wheat and barley
        final_classification_image_s1[wheat_index_logic] = 3
        # Non crop
        final_classification_image_s1[non_crop_pixels] = 4

        # Non crop
        # final_classification_image_s2[potato_classification_image] = 2
        final_classification_image_s2[non_crop_pixels] = 3

        return (final_classification_image_s1,
                final_classification_image_s2,
                self.crop_map
                )
