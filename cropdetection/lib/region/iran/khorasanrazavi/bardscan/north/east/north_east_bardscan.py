from ....base import IndexIranKhorasanRazavi
from remotesensingmathematica.rs_mathematica import DayFilePeak


class NorthEastBardscan(IndexIranKhorasanRazavi, DayFilePeak):

    def __init__(self, **kwargs):
        super().__init__(T=0.25,
                         peak=3,
                         wheat_index_threshold=1000,
                         maize_growth_period_threshold=150,
                         **kwargs)
