from ...base import IndexIranKhorasanRazavi
from remotesensingmathematica.rs_mathematica import DayFilePeak


class WestSarkhez(IndexIranKhorasanRazavi, DayFilePeak):

    def __init__(self, **kwargs):
        super().__init__(T=0.2,
                         peak=3,
                         wheat_index_threshold=500,
                         maize_growth_period_threshold=150,
                         **kwargs)
