from ...base import IndexIranKhorasanRazavi
from remotesensingmathematica.rs_mathematica import DayFilePeak


class NorthDargaz(IndexIranKhorasanRazavi, DayFilePeak):

    def __init__(self, **kwargs):
        super().__init__(T=0.2,
                         peak=2,
                         wheat_index_threshold=850,
                         maize_slope_threshold=200,
                         **kwargs)
