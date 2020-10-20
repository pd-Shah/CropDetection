import numpy as np


class OrchardV10():

    def __init__(self, orchard_threshold, **kwargs):
        self.orchard_threshold = orchard_threshold
        super().__init__(**kwargs)

    def orchard_index(self, NDVI, Rank_JulianDay_Orchard,
                      Previous_Classification_Image, Crop_Mask):
        '''
        This function detects orchards from other crops
            Inputs:
                NDVI: a 3D double array of time series of NDVIs from all
                    available images across the year.
                Rank_JulianDay_Orchard: a 1D array that depicts
                    min and max layers in NDVI timeseries for orchard detection
                Previous_Classification_Image: 2D binary matrix.
                Crop_Mask: 2D binary matrix that has value 1 for crop pixels

            Outputs:
                Orchard_matrix, a 2D matrix that has values of one for
                    orchard and zero for non - orchard pixels
        '''
        Orchard = np.zeros_like(NDVI[0])
        Orchard[
               (NDVI[np.min(Rank_JulianDay_Orchard):
                np.max(Rank_JulianDay_Orchard)] > self.orchard_threshold
                ).all()] = 1

        Orchard = np.logical_and(
                                np.logical_and(Orchard,
                                               Previous_Classification_Image),
                                Crop_Mask
                                )
        return Orchard.astype(np.bool)
