from ...base import IndexIranKhorasanRazavi
from remotesensingmathematica.rs_mathematica import DayFilePeak


class NorthGhochan(IndexIranKhorasanRazavi, DayFilePeak):

    def __init__(self, **kwargs):
        super().__init__(T=0.2,
                         peak=2,
                         wheat_index_threshold=600,
                         **kwargs)
