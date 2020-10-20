import numpy as np


class MaizeV10():

    def __init__(self,
                 maize_radiance_coefficient,
                 maize_slope_threshold,
                 # Turn maize_growth_period_threshold off:
                 #     np.inf
                 maize_growth_period_threshold,
                 **kwargs):

        self.maize_radiance_coefficient = maize_radiance_coefficient
        self.maize_slope_threshold = maize_slope_threshold
        self.maize_growth_period_threshold = maize_growth_period_threshold
        super().__init__(**kwargs)

    def maize_index(self, NDVI, julianday, Rank_JulianDay_S2,
                    numfiles, Max_Second_Season, Max_Second_Season_Logic,
                    Previous_Classification_Image):
        '''
        This function detects orchards from other crops

        Inputs:
            NDVI: a 3D double array of time series of NDVIs
                from all available images across the year.
            julianday: 1D array of juliandays of input files
                used in the script implementation;
            Max_Second_Season: a 2D double matrix that
                shows maximum NDVI values in second season;
            Min_Second_Season: a 2D double matrix that
                shows minimum NDVI values in second season;
            Previous_Classification_Image: 2D binary matrix.
            Rank_JulianDay_S2: layer number of
                first and last layer of second season.
            Crop_Mask: 2D binary matrix that has value 1 for crop pixels

        Outputs:
            Maize_matrix, a 2D matrix that has values of one
                for maize and zero for non - maize pixels
        '''
        min_Rank_JulianDay = np.min(Rank_JulianDay_S2)
        Rank_Max, _ = self.rank_find(
                                     NDVI,
                                     julianday,
                                     min_Rank_JulianDay,
                                     numfiles,
                                     Max_Second_Season
        )

        Rank_Min, julianday_min, Min_Second = self.min_find_ndvi(
                                                        NDVI,
                                                        julianday,
                                                        numfiles,
                                                        Rank_Max
        )

        Max_Optimum, _, JulianDay_Max_Optimum = self.find_max_optimum(
                                                                NDVI,
                                                                julianday,
                                                                Rank_Min,
                                                                Rank_Max
        )

        Slope = (
                    (Max_Optimum - Min_Second) *
                    self.maize_radiance_coefficient) / (
                                        julianday_min - JulianDay_Max_Optimum
                    )

        _, _, JulianDay_Min_Optimum = self.find_min_optimum(
                                                            NDVI,
                                                            julianday,
                                                            Rank_Max
        )

        Growth_Period = np.subtract(julianday_min, JulianDay_Min_Optimum)

        Maize_Index = np.logical_and(
                    np.logical_and(
                                    Max_Second_Season_Logic,
                                    Previous_Classification_Image
                    ),
                    np.logical_and(
                        Slope > self.maize_slope_threshold,
                        Growth_Period < self.maize_growth_period_threshold
                    ),

        )

        return Maize_Index.astype(np.bool)


class MaizeV9():

    def __init__(self, maize_radiance_coefficient,
                 maize_threshold, **kwargs):

        self.maize_radiance_coefficient = maize_radiance_coefficient
        self.maize_threshold = maize_threshold
        super().__init__(**kwargs)

    def maize_index(self, NDVI, julianday, Max_Second_Season,
                    Min_Second_Season, Rank_JulianDay_S2,
                    Previous_Classification_Image, Crop_Mask):
        '''
        This function detects orchards from other crops

            Inputs:
                NDVI: a 3D double array of time series of NDVIs from all
                     available images across the year.
                julianday: 1D array of juliandays of input files used in
                    the script implementation;
                Max_Second_Season: a 2D double matrix that shows maximum
                    NDVI values in second season;
                Min_Second_Season: a 2D double matrix that shows minimum
                    NDVI values in second season;
                Previous_Classification_Image: 2D binary matrix.
                Rank_JulianDay_S2: layer number of first and last
                    layer of second season.
                Crop_Mask: 2D binary matrix that has value 1 for crop pixels

            Outputs:
                Maize_matrix, a 2D matrix that has values of one
                    for maize and zero for non - maize pixels
        '''
        Maize = np.zeros_like(NDVI[0])
        Rank_Max = np.zeros_like(NDVI[0], dtype=np.int)
        Rank_Min = np.zeros_like(NDVI[0], dtype=np.int)

        julianday_max = np.zeros_like(NDVI[0], dtype=np.int)
        julianday_min = np.zeros_like(NDVI[0], dtype=np.int)

        for i in range(np.min(Rank_JulianDay_S2), np.max(Rank_JulianDay_S2)):
            Rank_Max[NDVI[i] == Max_Second_Season] = i
            Rank_Min[Min_Second_Season == NDVI[i]] = i

        for i in range(np.min(Rank_JulianDay_S2), np.max(Rank_JulianDay_S2)):

            julianday_max[NDVI[i] == Max_Second_Season] = (
                                                            julianday[Rank_Max]
                        )[NDVI[i] == Max_Second_Season]

            julianday_min[Min_Second_Season == NDVI[i]] = (
                                                            julianday[Rank_Min]
                        )[Min_Second_Season == NDVI[i]]

        julianday_range = np.subtract(julianday_max, julianday_min)

        Maize[np.divide(
                            (Max_Second_Season - Min_Second_Season) *
                            self.maize_radiance_coefficient, julianday_range
        ) > self.maize_threshold] = 1

        Maize = np.logical_and(
                        np.logical_and(Maize, Previous_Classification_Image),
                        Crop_Mask)

        return Maize.astype(np.bool)
