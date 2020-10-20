import numpy as np


class RiceV10():

    def __init__(self,
                 Rice_MinDay_Cultivation,
                 Rice_MaxDay_Cultivation, **kwargs):

        self.Rice_MaxDay_Cultivation = Rice_MaxDay_Cultivation
        self.Rice_MinDay_Cultivation = Rice_MinDay_Cultivation
        super().__init__(**kwargs)

    def Build_Rice_Index(self, NIR_Composite, NDVI_Composite,
                         Threshold, Julian_Days,
                         ):
        '''
        This function generates the canola classification image

        inputs:

        outputs:
            Rice detection image
            Rice classification image
        '''
        Rice_Cultivation_Bands_Logical = np.logical_and(
                                Julian_Days >= self.Rice_MinDay_Cultivation,
                                Julian_Days <= self.Rice_MaxDay_Cultivation
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

        return Rice_Classification_Image.astype(np.bool), Rice_Detection_Image


class RiceV11():

    def __init__(self, Rice_Cultivation_Start_Time,
                 Rice_Cultivation_Start_End, **kwargs):
        self.Rice_Cultivation_Start_End = Rice_Cultivation_Start_End
        self.Rice_Cultivation_Start_Time = Rice_Cultivation_Start_Time
        super().__init__(**kwargs)

    def rice_index(self, NIR_Composite, NDVI_Composite, Threshold,
                   Mountain_Mask, Julian_Days):
        '''
        This function generates the rice classification image

        inputs:

        outputs:
            Rice detection image
            Rice classification image
        '''
        Rice_Cultivation_Bands_Logical = np.logical_and(
                        Julian_Days >= self.Rice_Cultivation_Start_Time,
                        Julian_Days <= self.Rice_Cultivation_Start_End
         )

        Num_Bands = NDVI_Composite.shape[0]
        Total_Bands = np.array(range(Num_Bands))
        Rice_Cultivation_Bands = Total_Bands(Rice_Cultivation_Bands_Logical)

        # NDVI minimum bands for all image pixels
        # These bands correspond to rice cultivation time period
        NDVI_Min_Time = np.argmin(NDVI_Composite[Rice_Cultivation_Bands], axis=0)
        NDVI_Min_Values = np.min(NDVI_Composite[Rice_Cultivation_Bands], axis=0)
        NDVI_Min_Time = NDVI_Min_Time + (Rice_Cultivation_Bands[0] - 1)
        NDVI_Min_Values_Index = np.logical_not(NDVI_Min_Values >= 0.2)

        # NDVI maximum band
        NDVI_Max_Time = np.argmax(
                            NDVI_Composite[Rice_Cultivation_Bands[
                                                Rice_Cultivation_Bands.shape[0]
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
        Rice_Classification_Image = np.logical_and(
            Rice_Detection_Image < (Threshold * Image_Max),
            np.logical_and(NDVI_Mask,
                           np.logical_and(NDVI_Min_Values_Index, Mountain_Mask))
        )

        return Rice_Classification_Image.astype(np.bool), Rice_Detection_Image
