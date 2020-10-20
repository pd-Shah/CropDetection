from .src.alfalfa import AlfalfaV10
from .src.wheat import WheatV10
from .src.maize import MaizeV10
from .src.crop_mask import CropMaskV10


class IndexIranKhorasanRazavi(AlfalfaV10, WheatV10, MaizeV10, CropMaskV10):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
