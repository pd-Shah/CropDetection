import numpy as np


class PotatoV10():

    def __init__(self, potato_index_threshold,
                 potato_ndvi_threshold, **kwargs):
        self.potato_index_threshold = potato_index_threshold
        self.potato_ndvi_threshold = potato_ndvi_threshold

    def potato_index(self, NDVI, Slope,
                     Max_NIR, Min_Red, NIR_Harvest,
                     NIR_MIN, Previous_Classification_Image):
        '''
        This function calculates potato_index

            Input: MaxDayRank is a 2D matrix, NDVI
                is 3D time series of NDVI bands, Slope, Max_NIR
                Min_Red, NIR_Harvest, NIR_MIN are 2D matrix

            Output: Potato_Index is a 2D matrix
        '''
        Potato_Index = np.zeros_like(NDVI[0])

        for i in range(7, 14):
            Potato_Index[
                         NDVI[i] < self.potato_ndvi_threshold
            ] = Slope * Max_NIR / (Min_Red + NIR_Harvest) * NIR_MIN

        # Threshold for detection of potato pixels
        Potato_Index = np.logical_and(
                                Potato_Index > self.potato_index_threshold,
                                Previous_Classification_Image
        )

        return Potato_Index.astype(np.bool)
