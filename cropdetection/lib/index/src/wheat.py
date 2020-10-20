import numpy as np


class WheatV10():

    def __init__(self, wheat_index_threshold, **kwargs):
        self.wheat_index_threshold = wheat_index_threshold
        super().__init__(**kwargs)

    def wheat_index(self,
                    Red_Band_Greenness,
                    Red_Band_PostHarvest,
                    # Turn Off Previous_Classification_Image=1
                    Previous_Classification_Image,
                    # Turn Off crop_mask=1
                    crop_mask,
                    # Turn Off max_second_season_logic=0
                    max_second_season_logic,
                    # Trun off mask_wheat = 1
                    mask_wheat):
        '''
        This function calculates wheat index by using two bands of red, one for
            maximum greenness date and another for
        after harvest date; Then selects pixels that only wheat are cultivated
            in them and not wheat - maize.

        Inputs:
            Red_Band_Greenness: 2D matrix double;
                red band of maximum greenness date of wheat.
            Red_Band_PostHarvest: 2D matrix double;
                red band of post harvest date of wheat.

        Outputs:
            wheat_index_logic , a 2D binary matrix
        '''
        wheat_index = np.subtract(Red_Band_PostHarvest, Red_Band_Greenness)
        max_second_season_logic = np.logical_not(max_second_season_logic)

        wheat_index_logic = np.logical_and(
                            np.logical_and(
                                wheat_index > self.wheat_index_threshold,
                                mask_wheat
                            ),
                            np.logical_and(crop_mask,
                                           np.logical_and(
                                                 Previous_Classification_Image,
                                                 max_second_season_logic))
                                )

        return wheat_index_logic.astype(np.bool)
