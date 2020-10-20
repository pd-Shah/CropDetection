import numpy as np


class CropMaskV10():

    def __init__(self, crop_mask_ndvi_threshold, **kwargs):
        self.crop_mask_ndvi_threshold = crop_mask_ndvi_threshold
        super().__init__(**kwargs)

    def crop_mask(self, NDVI, numfiles):
        '''
        This function separates crop pixels from non crop pixels
            using thresholding NDVI TimeSeries;

            Inputs:
                NDVI TimeSeries - a 3D  double array (a matrix
                    with some layers as third dimension);

                numfiles: a scalar of number of files.

            Outputs:
                Crop_Mask: a 2D binary matrix that values of 1 indicates
                    crop pixels and values of 0 shows non crop pixels;
        '''
        Crop_Mask = np.zeros_like(NDVI[0])
        for i in range(numfiles):
            Crop_Mask[NDVI[i] > self.crop_mask_ndvi_threshold] = 1
        return Crop_Mask.astype(np.bool)
