import numpy as np


class AlfalfaV10():

    def __init__(self, alfalfa_ndvi_threshold,
                 alfalfa_index_threshold,
                 alfalfa_radiance_coefficient, **kwargs):

        self.alfalfa_ndvi_threshold = alfalfa_ndvi_threshold
        self.alfalfa_index_threshold = alfalfa_index_threshold
        self.alfalfa_radiance_coefficient = alfalfa_radiance_coefficient
        super().__init__(**kwargs)

    def alfalfa_index(self, NIR, Red, NDVI,
                      Rank_JulianDay_Harvest, Number_of_Files,
                      Previous_Classification_Image, Crop_Mask):

        '''
        This function calculates Alfalfa index by using NIR and Red TimeSeries

        Inputs:
            NIR TimeSeries,  a 3D double array of NIR (Near Infrared)
                bands (each band is for one date);
            Red TimeSeries, a 3D double array of
                Red bands (each band is for one date)
            Number_of_Files, number of bands or layers used in
                TimeSeries of Red and NIR
            Previous_Classification_Image: 2D binary matrix.
            Crop_Mask: 2D binary matrix that has value 1 for crop pixels
            Rank_JulianDay_Harvest: layer number of first and
                last layer of harvest time of wheat.

        Outputs:
            AlfalfaIndex, a 2D double matrix that has one value for each pixl
        '''
        AVERAGE_NIR = np.average(NIR, axis=0)
        AVERAGE_Red = np.average(Red, axis=0)

        NIR_Difference = np.zeros_like(NDVI[0], dtype=np.float)
        NIR_Difference_Final = np.zeros_like(NDVI[0], dtype=np.float)

        Red_Difference = np.zeros_like(NDVI[0], dtype=np.float)
        Red_Difference_Final = np.zeros_like(NDVI[0], dtype=np.float)

        for i in range(Number_of_Files-1):
            NIR_Difference[(NIR[i+1]-NIR[i]) < 0] = (
                2 * np.absolute(NIR[i + 1] - NIR[i]
                                ) / self.alfalfa_radiance_coefficient

            )[(NIR[i+1] - NIR[i]) < 0]

            NIR_Difference[(NIR[i+1]-NIR[i]) >= 0] = (
                np.absolute(NIR[i+1]-NIR[i])/self.alfalfa_radiance_coefficient
            )[(NIR[i+1] - NIR[i]) >= 0]

            Red_Difference = np.absolute(Red[i+1] - Red[i]
                                         ) / self.alfalfa_radiance_coefficient

            NIR_Difference_Final = NIR_Difference_Final + NIR_Difference
            Red_Difference_Final = Red_Difference_Final + Red_Difference

        Alfalfa_Index = (AVERAGE_NIR / AVERAGE_Red) * (
                            (NIR_Difference_Final * Red_Difference_Final)
                        )

        for j in range(1, np.max(Rank_JulianDay_Harvest)):
            Alfalfa_Index[NDVI[j] < self.alfalfa_ndvi_threshold] = 0

        Alfalfa_Index = np.logical_and(
                            np.logical_and(
                                (Alfalfa_Index > self.alfalfa_index_threshold),
                                Previous_Classification_Image),
                            Crop_Mask)

        return Alfalfa_Index.astype(np.bool)
