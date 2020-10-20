import numpy as np


class SugarBeetV10():

    def __init__(self, sugarbeet_ndvi_threshold, **kwargs):
        self.sugarbeet_ndvi_threshold = sugarbeet_ndvi_threshold
        super().__init__(**kwargs)

    def suger_beet_index(self, NDVI, Rank_JulianDay_Sugarbeet,
                         Previous_Classification_Image, Crop_Mask):
        '''
        This function detects orchards from other crops;
            Inputs:
                NDVI: a 3D double array of time series of NDVIs
                    from all available images across the year.

                Rank_JulianDay_Sugarbeet: a 1D array that depicts
                 min and max layers in NDVI timeseries for sugarbeet detection;

                Crop_Mask: 2D binary matrix that has value 1 for crop pixels;
                Previous_Classification_Image: 2D binary matrix.

            Outputs:
                Sugarbeet_matrix, a 2D matrix that has values of one
                    for sugarbeet and zero for non-sugarbeet pixels
          '''
        sugarbeet = np.zeros_like(NDVI[0])
        sugarbeet[(NDVI[min(Rank_JulianDay_Sugarbeet):
                        max(Rank_JulianDay_Sugarbeet)
                        ] > self.sugarbeet_ndvi_threshold).all()] = 1

        sugarbeet = np.logical_and(
                                np.logical_and(sugarbeet,
                                               Previous_Classification_Image),
                                Crop_Mask
                                )
        return sugarbeet.astype(np.bool)
