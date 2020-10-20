from ...base import IndexIranKhorasanRazavi
from remotesensingmathematica.rs_mathematica import DayFilePeak


class NorthNeyshabor(IndexIranKhorasanRazavi, DayFilePeak):

    def __init__(self, **kwargs):
        super().__init__(T=0.25,
                         wheat_index_threshold=1150,
                         maize_growth_period_threshold=150,
                         **kwargs)
