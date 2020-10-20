import numpy as np

from index.index import IndexIranAzarayjanGharbi

from remotesensingmathematica.rs_mathematica import (
                                        RSMathematicaIranAzarayjanGharbi,
)


class AzarbayjanGharbiBase(IndexIranAzarayjanGharbi,
                           RSMathematicaIranAzarayjanGharbi):
    def __init__(self,
                 NDVI, NIR, Red, InputPath,
                 Wheat_MinDay_Peak_Greenness=100,
                 Wheat_MaxDay_Peak_Greenness=140,
                 Wheat_MinDay_Harvest=180,
                 Wheat_MaxDay_Harvest=210,
                 First_Crop_Peak_MinDay=90,
                 First_Crop_Peak_MaxDay=160,
                 Second_Crop_Peak_MinDay=180,
                 Second_Crop_Peak_MaxDay=300,
                 Sugarbeet_MinDay=150,
                 Sugarbeet_MaxDay=280,
                 Orchard_MinDay=90,
                 Orchard_MaxDay=280,
                 MonthDays=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                 MonthDaysLeap=[31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                 alfalfa_ndvi_threshold=0.2,
                 alfalfa_index_threshold=0.75,
                 alfalfa_radiance_coefficient=10000,
                 crop_mask_threshold=0.35,
                 maize_radiance_coefficient=10000,
                 maize_threshold=150,
                 wheat_index_threshold=700,
                 orchard_threshold=0.5,
                 sugarbeet_ndvi_threshold=0.4,
                 ):

        self.NDVI = NDVI
        self.NIR = NIR
        self.Red = Red
        self.InputPath = InputPath
        self.Wheat_MinDay_Peak_Greenness = Wheat_MinDay_Peak_Greenness
        self.Wheat_MaxDay_Peak_Greenness = Wheat_MaxDay_Peak_Greenness
        self.Wheat_MinDay_Harvest = Wheat_MinDay_Harvest
        self.Wheat_MaxDay_Harvest = Wheat_MaxDay_Harvest
        self.First_Crop_Peak_MinDay = First_Crop_Peak_MinDay
        self.First_Crop_Peak_MaxDay = First_Crop_Peak_MaxDay
        self.Second_Crop_Peak_MinDay = Second_Crop_Peak_MinDay
        self.Second_Crop_Peak_MaxDay = Second_Crop_Peak_MaxDay
        self.Sugarbeet_MinDay = Sugarbeet_MinDay
        self.Sugarbeet_MaxDay = Sugarbeet_MaxDay
        self.Orchard_MinDay = Orchard_MinDay
        self.Orchard_MaxDay = Orchard_MaxDay
        self.MonthDays = MonthDays
        self.MonthDaysLeap = MonthDaysLeap
        self.crop_map = {"season 1":
                         {
                             "Wheat_and_barley_maize": 3,
                             'Wheat_and_barley':       2,
                             'Orchard':                4,
                             'Sugarbeet':              5,
                             'Alfalfa':                6,
                             'Maize':                  7,
                             'Noncrop':                8
                         }
                         }

        kwargs = {'alfalfa_ndvi_threshold': alfalfa_ndvi_threshold,
                  'alfalfa_index_threshold': alfalfa_index_threshold,
                  'alfalfa_radiance_coefficient': alfalfa_radiance_coefficient,
                  'crop_mask_threshold': crop_mask_threshold,
                  'maize_radiance_coefficient': maize_radiance_coefficient,
                  'maize_threshold': maize_threshold,
                  'wheat_index_threshold': wheat_index_threshold,
                  'orchard_threshold': orchard_threshold,
                  'sugarbeet_ndvi_threshold': sugarbeet_ndvi_threshold,
                  }

        super().__init__(**kwargs)

    def run(self, ):

        NDVI = self.NDVI
        NIR = self.NIR
        Red = self.Red
        InputPath = self.InputPath
        Wheat_MinDay_Peak_Greenness = self.Wheat_MinDay_Peak_Greenness
        Wheat_MaxDay_Peak_Greenness = self.Wheat_MaxDay_Peak_Greenness
        Wheat_MinDay_Harvest = self.Wheat_MinDay_Harvest
        Wheat_MaxDay_Harvest = self.Wheat_MaxDay_Harvest
        First_Crop_Peak_MinDay = self.First_Crop_Peak_MinDay
        First_Crop_Peak_MaxDay = self.First_Crop_Peak_MaxDay
        Second_Crop_Peak_MinDay = self.Second_Crop_Peak_MinDay
        Second_Crop_Peak_MaxDay = self.Second_Crop_Peak_MaxDay
        Sugarbeet_MinDay = self.Sugarbeet_MinDay
        Sugarbeet_MaxDay = self.Sugarbeet_MaxDay
        Orchard_MinDay = self.Orchard_MinDay
        Orchard_MaxDay = self.Orchard_MaxDay
        MonthDays = self.MonthDays
        MonthDaysLeap = self.MonthDaysLeap

        # Counting number of files and dates of them from input folder determined by user above
        #Counting number of files
        numfiles=self.NumFiles(InputPath)

        #Extracting dates of files
        FileDates=self.FileNames(InputPath)

        # Conversion of Image dates to julian days using "JulianDay" function
        julianday=[int(self.julianday(i, MonthDays, MonthDaysLeap)) for i in FileDates]
        julianday=np.array(sorted(julianday))

        Band_Number_Wheat_Peak=julianday[np.logical_and(julianday>Wheat_MinDay_Peak_Greenness, julianday<Wheat_MaxDay_Peak_Greenness)]
        Band_Number_Wheat_Harvest=julianday[np.logical_and(julianday>Wheat_MinDay_Harvest,julianday<Wheat_MaxDay_Harvest)]
        Band_Number_First_Crop=julianday[np.logical_and(julianday>First_Crop_Peak_MinDay,julianday<First_Crop_Peak_MaxDay)]
        Band_Number_Second_Crop=julianday[np.logical_and(julianday>Second_Crop_Peak_MinDay,julianday<Second_Crop_Peak_MaxDay)]

        Band_Number_Sugarbeet=julianday[np.logical_and(julianday>Sugarbeet_MinDay,julianday<Sugarbeet_MaxDay)]
        Band_Number_Orchard=julianday[np.logical_and(julianday>Orchard_MinDay,julianday<Orchard_MaxDay)]

        # Determination of ranks of wheat peak and harvest, first season and second season dates

        Rank_JulianDay_Peak=self.RankJulianDay(julianday,Band_Number_Wheat_Peak)

        Rank_JulianDay_Harvest=self.RankJulianDay(julianday,Band_Number_Wheat_Harvest)
        Rank_JulianDay_S1=self.RankJulianDay(julianday,Band_Number_First_Crop)
        Rank_JulianDay_S2=self.RankJulianDay(julianday,Band_Number_Second_Crop)
        Rank_JulianDay_Sugarbeet=self.RankJulianDay(julianday,Band_Number_Sugarbeet)
        Rank_JulianDay_Orchard=self.RankJulianDay(julianday,Band_Number_Orchard)

        # Finding appropriate red bands for wheat index
        if len(Rank_JulianDay_Peak)==1:
            Red_Peak=Red[Rank_JulianDay_Peak[0]]
        else :
            Red_Peak=Red[np.min(Rank_JulianDay_Peak): np.max(Rank_JulianDay_Peak)+1]
            Red_Peak=np.min(Red_Peak,axis=0)

        if len(Rank_JulianDay_Harvest)==1:
            Red_Harvest=Red[Rank_JulianDay_Harvest]
        else:
            Red_Harvest=Red[np.min(Rank_JulianDay_Harvest):np.max(Rank_JulianDay_Harvest)+1]
            Red_Harvest=np.min(Red_Harvest,axis=0)

        #  Determination of maximum NDVI for first and second season
        if len(Rank_JulianDay_S1)==1:
            First_Season=NDVI[Rank_JulianDay_S1[0]]
        else:
            First_Season=NDVI[np.min(Rank_JulianDay_S1):np.max(Rank_JulianDay_S1)+1]
            Max_First_Season=np.max(First_Season,axis=0)

        if len(Rank_JulianDay_S2)==1:
            Second_Season=NDVI[Rank_JulianDay_S2[0]]
        else:
            Second_Season=NDVI[np.min(Rank_JulianDay_S2):np.max(Rank_JulianDay_S2)+1]
            Max_Second_Season=np.max(Second_Season,axis=0)
            Min_Second_Season=np.min(Second_Season,axis=0)

        # Max_Second_Season=np.max(First_Season)
        # Min_Second_Season=np.min(Second_Season)
        # Crop mask (Separation of crops based on NDVI threshold)
        Crop_Mask=self.crop_mask(NDVI,numfiles)

        # a Predetermined 2D matrix with values of 1
        Previous_Classification_Image=np.ones_like(NDVI[0])

        # Detection of pixels with NDVI in second season greater than 0.35
        Max_Second_Season_Logic=Max_Second_Season>0.35

        # Wheat index calculation using Red bands selected in appropriate dates
        Wheat_Index_logic=self.wheat_index(Red_Band_Greenness=Red_Peak, Red_Band_PostHarvest=Red_Harvest, Crop_Mask=Crop_Mask, Max_Second_Season_Logic=Max_Second_Season_Logic)
        Previous_Classification_Image[Wheat_Index_logic]=0

        # Detection of double_cropping pixels
        Wheat_Double_Crop=self.wheat_index(Red_Band_Greenness=Red_Peak, Red_Band_PostHarvest=Red_Harvest, Crop_Mask=Crop_Mask)
        Double_Cropping=self.double_crop(Wheat_Double_Crop, Max_Second_Season_Logic, Previous_Classification_Image)
        Previous_Classification_Image[Double_Cropping]=0

        # Detection of Orchards
        Orchard=self.orchard_index(NDVI, Rank_JulianDay_Orchard, Previous_Classification_Image, Crop_Mask)
        Previous_Classification_Image[Orchard]=0

        # Detection of Sugarbeet
        sugarbeet=self.suger_beet_index(NDVI, Rank_JulianDay_Sugarbeet, Previous_Classification_Image, Crop_Mask)
        Previous_Classification_Image[sugarbeet]=0

        # Calculation of alfalfa index for detecting alfalfa fields
        Alfalfa_Index=self.alfalfa_index( NIR, Red, NDVI, Rank_JulianDay_Harvest, numfiles, Previous_Classification_Image, Crop_Mask)
        Previous_Classification_Image[Alfalfa_Index]=0

        # Detection of Maize
        Maize=self.maize_index(NDVI,julianday,Max_Second_Season,Min_Second_Season,Rank_JulianDay_S2,Previous_Classification_Image,Crop_Mask)
        Previous_Classification_Image[Maize]=0

        # Detecting non crop pixels
        Non_Crop_Pixels=np.logical_not(Crop_Mask)

        # Final Crop Map; pixels with value 1 are other crops like sunflower and pumpkin
        Previous_Classification_Image[Double_Cropping]=3              #Wheat and barley - maize
        Previous_Classification_Image[Wheat_Index_logic]=2            #Wheat and barley
        Previous_Classification_Image[Orchard]=4                      #Orchard
        Previous_Classification_Image[sugarbeet]=5                    #Sugarbeet
        Previous_Classification_Image[Alfalfa_Index]=6                #Alfalfa
        Previous_Classification_Image[Maize]=7                        #Maize
        Previous_Classification_Image[Non_Crop_Pixels]=8              #Non crop

        return {
         'final_classification_image_s1': Previous_Classification_Image,
         'color_map': self.crop_map,
        }
