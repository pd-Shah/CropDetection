from __future__ import division, print_function
import warnings
import rasterio
import numpy as np
import glob
import os


def Build_Alfalfa_Index(NIR, Red, NDVI, Rank_JulianDay_Harvest, Number_of_Files, Previous_Classification_Image, Crop_Mask):
    '''
    This function calculates Alfalfa index by using NIR and Red TimeSeries

        Inputs:
            NIR TimeSeries,  a 3D double array of NIR (Near Infrared) bands (each band is for one date);
            Red TimeSeries, a 3D double array of Red bands (each band is for one date)
            Number_of_Files, number of bands or layers used in TimeSeries of Red and NIR
            Previous_Classification_Image: 2D binary matrix.
            Crop_Mask: 2D binary matrix that has value 1 for crop pixels
            Rank_JulianDay_Harvest: layer number of first and last layer of harvest time of wheat.

        Outputs:
            AlfalfaIndex, a 2D double matrix that has one value for each pixl
    '''

    AVERAGE_NIR=np.mean(NIR,axis=0)
    AVERAGE_Red=np.mean(Red,axis=0)

    NIR_Difference=       np.zeros_like(NDVI[0],dtype=np.float)
    NIR_Difference_Final= np.zeros_like(NDVI[0],dtype=np.float)

    Red_Difference=       np.zeros_like(NDVI[0], dtype=np.float)
    Red_Difference_Final= np.zeros_like(NDVI[0], dtype=np.float)

    for i in range(Number_of_Files-1):
        NIR_Difference[(NIR[i+1]-NIR[i])<0]=np.divide( 2 * np.absolute(NIR[i+1]-NIR[i]), 10000)[(NIR[i+1]-NIR[i])<0]
        NIR_Difference[(NIR[i+1]-NIR[i])>=0]=np.divide(np.absolute(NIR[i+1]-NIR[i]),10000)[(NIR[i+1]-NIR[i])>=0]

        Red_Difference[np.subtract(NIR[i+1],NIR[i])<0]= np.divide(np.absolute(NIR[i+1]-NIR[i]),10000)[np.subtract(NIR[i+1],NIR[i])<0]

        NIR_Difference_Final= NIR_Difference_Final + NIR_Difference
        Red_Difference_Final= Red_Difference_Final + Red_Difference

    Alfalfa_Index= np.divide( AVERAGE_NIR, AVERAGE_Red) * np.multiply( NIR_Difference_Final, Red_Difference_Final )

    for j in range(1, np.max(Rank_JulianDay_Harvest)):
        Alfalfa_Index[NDVI[j]<0.2]=0

    Alfalfa_Index=np.logical_and(np.logical_and(
                                                ( Alfalfa_Index > 0.75 ), Previous_Classification_Image ),Crop_Mask)

    return Alfalfa_Index


def Build_Wheat_Index(Red_Band_Greenness, Red_Band_PostHarvest, Previous_Classification_Image):
    '''
    This function calculates wheat index by using two bands of red, one for maximum greenness date and another for
    after harvest date; Then selects pixels that only wheat are cultivated in them and not wheat - maize.

        Inputs:
            Red_Band_Greenness: 2D matrix double; red band of maximum greenness date of wheat.
            Red_Band_PostHarvest: 2D matrix double; red band of post harvest date of wheat.

        Outputs:
            wheat_index_logic , a 2D binary matrix
    '''
    wheat_index = np.subtract(Red_Band_PostHarvest, Red_Band_Greenness)

    # Detection of pixels with wheat_index greater than 700
    wheat_index_logic = np.logical_and(wheat_index > 900,
                                       Previous_Classification_Image)

    return wheat_index_logic


def julianday(name, MonthDays, MonthDaysLeap):
    '''
    This function converts image dates to Julian Day
        Input:
            FileDates (Image_file_Dates, e.g 20170508, always is 8 digits)

        Output:
            1D numeric array of images julian days, minimum is 1 and maximum is 366
    '''

    # Calculation of julian day based on dates of images
    for i in range(1,13):
        if int(name[4:6])==i and i>1:
            if int(name[:4])%4==0:
                julianday=int(name[6:8])+sum(MonthDays[:i-1])

            elif int(name[:4])%4!=0:
                julianday=int(name[6:8])+sum(MonthDaysLeap[0:i-1])

        elif int(name[4:6])==i and i<=1:
            julianday=int(name[6:8])

    return julianday


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

    Rank_Max=       np.zeros_like(NDVI[0], dtype=np.int)
    julianday_max=  np.zeros_like(NDVI[0], dtype=np.int)

    for i in range(start, last):
        Rank_Max  [ NDVI[i] == Max_Second_Season ]= i
        julianday_max [ NDVI[i] == Max_Second_Season] = (julianday[ Rank_Max ]) [ NDVI[i] == Max_Second_Season ]

    return Rank_Max, julianday_max


def min_find (NDVI, julianday, start, last):
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
    Rank_Min=       np.zeros_like(NDVI[0], dtype=np.int)
    julianday_min=  np.zeros_like(NDVI[0], dtype=np.int)
    Min_Second=     np.zeros_like(NDVI[0], dtype=np.float)

    for i in range(NDVI.shape[1]):
        for j in range(NDVI.shape[2]):
            m=min([start, last[i,j]])
            M=max([start, last[i,j]])

            for L in range(m,M):
                if NDVI[L, i, j] < 0.2:
                    Min_Second [i,j] = NDVI [L,i,j]
                    Rank_Min [i,j] = L
                    julianday_min [i,j] = julianday [Rank_Min [i,j]]
                    break

    return Rank_Min, julianday_min, Min_Second


def Build_Maize_Index(NDVI, julianday, Rank_JulianDay_S2, numfiles, Max_Second_Season, Max_Second_Season_Logic, Previous_Classification_Image):
    '''
    This function detects orchards from other crops

        Inputs:
            NDVI: a 3D double array of time series of NDVIs from all available images across the year.
            julianday: 1D array of juliandays of input files used in the script implementation;
            Max_Second_Season: a 2D double matrix that shows maximum NDVI values in second season;
            Min_Second_Season: a 2D double matrix that shows minimum NDVI values in second season;
            Previous_Classification_Image: 2D binary matrix.
            Rank_JulianDay_S2: layer number of first and last layer of second season.
            Crop_Mask: 2D binary matrix that has value 1 for crop pixels

        Outputs:
            Maize_matrix, a 2D matrix that has values of one for maize and zero for non - maize pixels
    '''
    min_Rank_JulianDay= np.min(Rank_JulianDay_S2)
    Rank_Max, _ =       rank_find(NDVI, julianday, min_Rank_JulianDay, numfiles, Max_Second_Season)

    Rank_Min, julianday_min, Min_Second=   min_find( NDVI, julianday, numfiles, Rank_Max)
    Max_Optimum, _, JulianDay_Max_Optimum= Find_Max_Optimum(NDVI, julianday, Rank_Min, Rank_Max)

    Slope = ( (Max_Optimum - Min_Second) * 10000) / (julianday_min - JulianDay_Max_Optimum)

    Maize_Index=np.logical_and(
                        np.logical_and( Max_Second_Season_Logic, Previous_Classification_Image ),
                        Slope > 150 )
    return Maize_Index


def RankJulianDay(julianday,crop_growth_days):
    '''
    This function extracts ranks of julian days

        Inputs :
        julianday is a 1D array of juliandays of input files used in the script implementation
        crop_growth_days is a 1D array of julian days of files in desired period

        Outputs :
        Rank_JulianDay is a 1D array of ranks (of desired layers)
    '''
    julianday=julianday.tolist()

    if len(crop_growth_days)==1:
        c_p=julianday.index(crop_growth_days[0])
        Rank_JulianDay=np.array([c_p])

    else:
        min_peak=np.min(crop_growth_days)
        max_peak=np.max(crop_growth_days)
        c_p_min=julianday.index(min_peak)
        c_p_max=julianday.index(max_peak)
        Rank_JulianDay=np.array([c_p_min, c_p_max])
    return Rank_JulianDay


def CropMask(NDVI, numfiles):
    '''
    This function separates crop pixels from non crop pixels using thresholding NDVI TimeSeries;

        Inputs:
            NDVI TimeSeries - a 3D  double array (a matrix with some layers as third dimension);
            numfiles: a scalar of number of files.

        Outputs:
            Crop_Mask: a 2D binary matrix that values of 1 indicates crop pixels and values of 0 shows non crop pixels;
    '''
    Crop_Mask=np.zeros_like(NDVI[0])
    for i in range (numfiles):
        Crop_Mask[NDVI[i]>0.3]=1
    return Crop_Mask


def NumFiles(InputPath):
    '''
    This function counts number of sentinel2 files in the InputPath
        Input:
            InputPath (path for input directory that images are located, for example: B:\Khoy\Sentinel2)
        Output:
            Number of files in InputPath
    '''
    with open(InputPath) as name_files:
        counts = len(name_files.readlines())
    return counts


def FileNames(InputPath):
    '''
    This function acquires dates of sentinel_2 files in the folder
        input:
            InputPath (path for input directory that images are located, for example: B:\Khoy\Sentinel2)
        Output:
            1D numeric (double) vector of image dates
    '''
    # should import os
    with open(InputPath) as file_names:
        dates = [i[11:19] for i in file_names if i != '\n']
    return dates


def Find_Peak(T, peak, Alfalfa_Index, NDVI):

    alfalfa_peak=  np.zeros_like(NDVI[0])
    args=          np.argwhere(Alfalfa_Index)
    temp=          NDVI[:, args[:, 0], args[:, 1]].swapaxes(1,0)

    for index,item in enumerate(temp):
        pks=detect_peaks(item, mph=T)
        if len(pks) > peak:
            i,j=args[index]
            alfalfa_peak[i,j]=1

    return alfalfa_peak.astype(np.int)


def Find_Max_Optimum(NDVI,  julianday, Rank_Min, Rank_Max):
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
            for L in range(Rank_Min[i,j], Rank_Max[i,j], -1):
                if L < 1:
                    break

                if NDVI [L, i, j] >  0.6:
                    Max_Optimum [i, j] = NDVI [L, i, j]
                    Rank_Max_Optimum [i, j] = L
                    JulianDay_Max_Optimum [i, j] = julianday[int(Rank_Max_Optimum [i, j])]
                    break

    return Max_Optimum, Rank_Max_Optimum, JulianDay_Max_Optimum


def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising', kpsh=False, valley=False, show=False, ax=None):

    """Detect peaks in data based on their amplitude and other features.

    Parameters
    ----------
    x : 1D array_like
        data.
    mph : {None, number}, optional (default = None)
        detect peaks that are greater than minimum peak height.
    mpd : positive integer, optional (default = 1)
        detect peaks that are at least separated by minimum peak distance (in
        number of data).
    threshold : positive number, optional (default = 0)
        detect peaks (valleys) that are greater (smaller) than `threshold`
        in relation to their immediate neighbors.
    edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    kpsh : bool, optional (default = False)
        keep peaks with same height even if they are closer than `mpd`.
    valley : bool, optional (default = False)
        if True (1), detect valleys (local minima) instead of peaks.
    show : bool, optional (default = False)
        if True (1), plot data in matplotlib figure.
    ax : a matplotlib.axes.Axes instance, optional (default = None).

    Returns
    -------
    ind : 1D array_like
        indeces of the peaks in `x`.
    """

    x = np.atleast_1d(x).astype('float64')
    if x.size < 3:
        return np.array([], dtype=int)
    if valley:
        x = -x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan] = np.inf
        dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan-1, indnan+1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size-1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = np.min(np.vstack([x[ind]-x[ind-1], x[ind]-x[ind+1]]), axis=0)
        ind = np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                    & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = np.nan
        if valley:
            x = -x
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind)

    return ind


def _plot(x, mph, mpd, threshold, edge, valley, ax, ind):
    """Plot results of the detect_peaks function, see its help."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib is not available.')
    else:
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(8, 4))

        ax.plot(x, 'b', lw=1)
        if ind.size:
            label = 'valley' if valley else 'peak'
            label = label + 's' if ind.size > 1 else label
            ax.plot(ind, x[ind], '+', mfc=None, mec='r', mew=2, ms=8,
                    label='%d %s' % (ind.size, label))
            ax.legend(loc='best', framealpha=.5, numpoints=1)
        ax.set_xlim(-.02*x.size, x.size*1.02-1)
        ymin, ymax = x[np.isfinite(x)].min(), x[np.isfinite(x)].max()
        yrange = ymax - ymin if ymax > ymin else 1
        ax.set_ylim(ymin - 0.1*yrange, ymax + 0.1*yrange)
        ax.set_xlabel('Data #', fontsize=14)
        ax.set_ylabel('Amplitude', fontsize=14)
        mode = 'Valley detection' if valley else 'Peak detection'
        ax.set_title("%s (mph=%s, mpd=%d, threshold=%s, edge='%s')"
                     % (mode, str(mph), mpd, str(threshold), edge))
        # plt.grid()
        plt.show()


def Build_Rice_Index(NIR_Composite, NDVI_Composite, Threshold, Julian_Days,
                     Rice_MinDay_Cultivation=160, Rice_MaxDay_Cultivation=190,
                     ):
    '''
    This function generates the canola classification image

    inputs:
        Red band image cube
        NIR band image cube
        NDVI band image cube
        Flowering month number

    outputs:
        Rice detection image
        Rice classification image
    '''
    Rice_Cultivation_Bands_Logical = np.logical_and(
                                        Julian_Days >= Rice_MinDay_Cultivation,
                                        Julian_Days <= Rice_MaxDay_Cultivation
                                        )
    Num_Bands = NDVI_Composite.shape[0]
    Total_Bands = np.array(Num_Bands)
    Rice_Cultivation_Bands = Total_Bands(Rice_Cultivation_Bands_Logical)

    # NDVI minimum bands for all image pixels
    # These bands correspond to rice cultivation time period
    NDVI_Min_Time = np.argmin(NDVI_Composite[Rice_Cultivation_Bands], axis=0)
    NDVI_Min_Time = NDVI_Min_Time + (Rice_Cultivation_Bands[0] - 1)

    # NDVI maximum band
    NDVI_Max_Time = np.argmax(
                        NDVI_Composite[Rice_Cultivation_Bands[
                                            Rice_Cultivation_Bands.shape[0]-1
                                            ]:
                                       ], axis=0)

    NDVI_Max_Time = NDVI_Max_Time + (
                                      Rice_Cultivation_Bands[
                                         Rice_Cultivation_Bands.shape[0]
                                         ] - 1)
    Rice_Detection_Image = np.sum(NIR_Composite[NDVI_Min_Time: NDVI_Max_Time],
                                  axis=0)

    # Masking non-vegetation pixels
    NDVI_Mask = (np.sum(NDVI_Composite[NDVI_Min_Time:] > 0.4, axis=0)
                 ).astype(np.bool)

    Image_Max = np.max(Rice_Detection_Image)
    Rice_Classification_Image = np.logical_and(Rice_Detection_Image <
                                               (Threshold * Image_Max),
                                               NDVI_Mask)

    return Rice_Classification_Image, Rice_Detection_Image
