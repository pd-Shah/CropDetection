from ..base import IndexIranKhorasanRazavi
from remotesensingmathematica.rs_mathematica import DayFilePeak


class Fariman(IndexIranKhorasanRazavi, DayFilePeak):

    def __init__(self, **kwargs):
        super().__init__(T=0.15,
                         peak=3,
                         wheat_index_threshold=1400,
                         maize_slope_threshold=200,
                         maize_growth_period_threshold=150,
                         **kwargs)
