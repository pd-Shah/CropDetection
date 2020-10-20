import numpy as np


class DoubleCropV10():

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def double_crop(self,
                    wheat_index,
                    Max_Second_Season_Logic,
                    Previous_Classification_Image):
        '''
        This function detects double cropping pixels

            Inputs:
                wheat_index: 2D binary matrix
                Max_Second_Season_Logic: 2D binary matrix
                Previous_Classification_Image: 2D binary matrix

            Outputs:
                double crop, a 2D binary matrix
        '''
        double_cropping_final = np.logical_and(
                                            np.logical_and(
                                                wheat_index,
                                                Max_Second_Season_Logic),
                                            Previous_Classification_Image)

        return double_cropping_final.astype(np.bool)
