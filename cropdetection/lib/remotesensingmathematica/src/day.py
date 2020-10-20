import numpy as np


class Day():

    @staticmethod
    def julianday(name, MonthDays, MonthDaysLeap):
        '''
        This function converts image dates to Julian Day
        Input:
            FileDates (Image_file_Dates, e.g 20170508, always is 8 digits)

        Output:
            1D numeric array of images julian days, minimum is 1 and maximum is 366
        '''

        # Calculation of julian day based on dates of images
        for i in range(1, 13):
            if int(name[4:6]) == i and i > 1:
                if int(name[:4]) % 4 == 0:
                    julianday = int(name[6:8])+sum(MonthDays[:i-1])
                elif int(name[:4]) % 4 != 0:
                    julianday = int(name[6:8]) + sum(MonthDaysLeap[0:i-1])
            elif name[4:6] == i and i <= 1:
                julianday = int(name[6:8])

        return julianday

    @staticmethod
    def min_find_ndvi(NDVI, julianday, start, last):
        '''
        INPUTS:
           R: Coordinate System Information
           NDVI: stack
           julianday
           start: the beginning day of the season
           last: the last day of the season

         OUTPUTS:
           Rank_Min: minimum ndvi band number
           julianday_min: minimum ndvi Julian day
           Min_Second: minimum ndvi value in the second season
        '''
        Rank_Min=      np.zeros_like(NDVI[0], dtype=np.int)
        julianday_min= np.zeros_like(NDVI[0], dtype=np.int)
        Min_Second=    np.zeros_like(NDVI[0], dtype=np.float)

        for i in range(NDVI.shape[1]):
            for j in range(NDVI.shape[2]):
                m = min([start, last[i, j]])
                M = max([start, last[i, j]])

                for L in range(m, M):
                    if NDVI[L, i, j] < 0.2:
                        Min_Second[i, j] = NDVI[L, i, j]
                        Rank_Min[i, j] = L
                        julianday_min[i, j] = julianday[Rank_Min[i, j]]
                        break

        return Rank_Min, julianday_min, Min_Second

    @staticmethod
    def rank_find(NDVI,  julianday, start, last, Max_Second_Season):
        '''
        INPUTS:
           R: Coordinate System Information
           NDVI: stack
           julianday
           start: the beginning day of the season
           last: the last day of the season
           Max_Second_Season: maximum ndvi band value in the second season

        OUTPUTS:
           Rank_Max: maximum ndvi band number
           julianday_max: maximum ndvi Julian day
        '''

        Rank_Max =      np.zeros_like(NDVI[0], dtype=np.int)
        julianday_max = np.zeros_like(NDVI[0], dtype=np.int)

        for i in range(start, last):
            Rank_Max[NDVI[i] == Max_Second_Season] = i
            julianday_max[NDVI[i] == Max_Second_Season] = (
                                                            julianday[Rank_Max]
            )[NDVI[i] == Max_Second_Season]

        return Rank_Max, julianday_max

    @staticmethod
    def rank_julian_day(julianday, crop_growth_days):
        '''
        This function extracts ranks of julian days
        Inputs :
            julianday is a 1D array of juliandays of input
            files used in the script implementation
            crop_growth_days is a 1D array of julian days
            of files in desired period

        Outputs :
            Rank_JulianDay is a 1D array of ranks (of desired layers)
        '''
        julianday = julianday.tolist()

        if len(crop_growth_days) == 1:
            c_p = julianday.index(crop_growth_days[0])
            Rank_JulianDay = np.array([c_p])

        else:
            min_peak = np.min(crop_growth_days)
            max_peak = np.max(crop_growth_days)
            c_p_min = julianday.index(min_peak)
            c_p_max = julianday.index(max_peak)
            Rank_JulianDay = np.array([c_p_min, c_p_max])
        return Rank_JulianDay.astype(int)

    @staticmethod
    def find_max_optimum(NDVI, julianday, Rank_Min, Rank_Max):
        '''
            INPUTS:
                R: Coordinate System Information
                NDVI: stack
                julianday
                Rank_Min: minimum ndvi band number
                Rank_Max: maximum ndvi band number

            OUTPUTS:
                Max_Optimum: The last ndvi max before the first ndvi min
                Rank_Max_Optimum: the ndvi band number for Max_Optimum
                JulianDay_Max_Optimum: Julian day for Rank_Max_Optimum
        '''
        Max_Optimum=           np.zeros_like(NDVI[0])
        Rank_Max_Optimum=      np.zeros_like(NDVI[0])
        JulianDay_Max_Optimum= np.zeros_like(NDVI[0])

        for i in range(NDVI.shape[1]):
            for j in range(NDVI.shape[2]):
                for L in range(Rank_Min[i, j], Rank_Max[i, j], -1):
                    if L < 1:
                        break

                    if NDVI[L, i, j] > 0.6:
                        Max_Optimum[i, j] = NDVI[L, i, j]
                        Rank_Max_Optimum[i, j] = L
                        JulianDay_Max_Optimum[i, j] = julianday[int(Rank_Max_Optimum[i, j])]
                        break

        return Max_Optimum, Rank_Max_Optimum, JulianDay_Max_Optimum

    @staticmethod
    def min_find_red(MaxDayRank, red):
        '''
        This function Finds minimum of red band
            time series correspoding to MaxDayRank

            Input: MaxDayRank is a 2D matrix and red is
                3D time series of red bands

            Output: Min_Red is a 2D matrix
        '''
        MaxDayRank = MaxDayRank.astype(np.int)

        Min_Red = np.zeros_like(MaxDayRank)
        for i in range(MaxDayRank.shape[0]):
            for j in range(MaxDayRank.shape[1]):
                if MaxDayRank[i, j] > 0:
                    Min_Red[i, j] = red[MaxDayRank[i, j], i, j]
        return Min_Red

    @staticmethod
    def find_slope(MaxDayRank, nir):
        '''
        This function calculates slope of nir values from
            cultivation time of potato to peak stage

            Input: MaxDayRank is a 2D matrix and
                nir is 3D time series of nir bands

            Output: Slop is a 2D matrix
        '''
        slope = np.zeros_like(MaxDayRank)
        Slop = np.zeros_like(MaxDayRank)
        MaxDayRank = MaxDayRank.astype(np.int)
        for i in range(MaxDayRank.shape[0]):
            for j in range(MaxDayRank.shape[1]):
                if MaxDayRank[i, j] > 0:
                    for t in range(2, MaxDayRank[i, j]):
                        slope[i, j] = nir[t, i, j] - nir[t-1, i, j]
                        Slop[i, j] = Slop[i, j] + slope[i, j]
                else:
                    Slop[i, j] = 0
        return Slop

    @staticmethod
    def find_max_day(inputfile, max_file):
        '''
        This function Finds the rank of the layer that
            has the maximum value in time series

            Input: inputfile is a 3D matrix and max_file
                is 2D time series of red bands

            Output: MaxDayRank is a 2D matrix
        '''
        MaxDayRank = np.zeros_like(inputfile[0])
        for i in range(1, 14):
            MaxDayRank[max_file == inputfile[i]] = i

        return MaxDayRank

    @staticmethod
    def find_min_optimum(NDVI,  julianday, Rank_Max):
        '''
        INPUTS:
            R: Coordinate System Information
            NDVI: stack
            julianday
            Rank_Min: minimum ndvi band number
            Rank_Max: maximum ndvi band number

        OUTPUTS:
            Max_Optimum: The last ndvi max before the first ndvi min
            Rank_Max_Optimum: the ndvi band number for Max_Optimum
            JulianDay_Max_Optimum: Julian day for Rank_Max_Optimum
        '''
        Min_Optimum=           np.zeros_like(NDVI[0])
        Rank_Min_Optimum=      np.zeros_like(NDVI[0])
        JulianDay_Min_Optimum= np.zeros_like(NDVI[0])

        for i in range(NDVI.shape[1]):
            for j in range(NDVI.shape[2]):
                for L in range( Rank_Max[i,j], -1):
                    if L < 1:
                        break

                    if NDVI [L, i, j] <  0.25:
                        Min_Optimum [i, j] = NDVI [L, i, j]
                        Rank_Min_Optimum [i, j] = L
                        JulianDay_Min_Optimum [i, j] = julianday[1,int(Rank_Min_Optimum [i, j])]
                        break

        return Min_Optimum, Rank_Min_Optimum, JulianDay_Min_Optimum

    @staticmethod
    def find_max_day_rank(MaxDayRank):
        '''
        This function puts the MaxDayRank values
             of non - potato crops to zero

            Input: inputfile is a 2D matrix (MaxDayRank)

            Output: MaxDayRank is a 2D matrix
        '''
        Max_Potato = np.zeros_like(MaxDayRank)
        Max_Potato[
                    np.logical_and(MaxDayRank > 4,
                                   MaxDayRank < 12)
         ] = MaxDayRank[
                      np.logical_and(
                          MaxDayRank > 4,
                          MaxDayRank < 12
                      )
            ]

        Max_Potato[
                    np.logical_not(
                        np.logical_and(MaxDayRank > 4, MaxDayRank < 12)
                    )
        ] = 0

        return Max_Potato
