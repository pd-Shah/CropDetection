import numpy as np


class CanolaV10():

    def __init__(self, NDVI_canola_threshold,
                 canola_index_threshold, **kwargs):
        self.NDVI_canola_threshold = NDVI_canola_threshold
        self.canola_index_threshold = canola_index_threshold

    def canola_index(self, NIR_canola, Red_canola, Green_canola,
                     NDVI_canola, Previous_Classification_Image):
        '''
        this function detects canola based on 3 bands
            of flowering date of canola and NDVI;

        inputs:
            NIR_canola - a 2D array matrix;
                NIR band of a date in canola flowering season;
            Red_canola - a 2D array matrix;
                Red band of a date in canola flowering season;
            Green_canola - a 2D array matrix;
                Green band of a date in canola flowering season;
        outputs:
            final_canola - a 2D Binary matrix;
        '''
        NIR_canola[NIR_canola == np.max(NIR_canola)] = 0

        canola_index = NIR_canola * (Red_canola + Green_canola)

        # pixels with NDVI values of greater than 0.4
        NDVI_max = NDVI_canola > self.NDVI_canola_threshold

        # finds maximum value of canola_index
        max_canola = np.max(canola_index)

        # detection of canola by given percentage of maximum value
        canola_classification = canola_index > (self.canola_index_threshold *
                                                max_canola
                                                )

        final_canola = np.logical_and(NDVI_max,
                                      np.logical_and(canola_classification,
                                                     Previous_Classification_Image)
                                      )
        return final_canola.astype(np.bool)
