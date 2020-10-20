from ...base import IndexIranKhorasanRazavi
from remotesensingmathematica.rs_mathematica import DayFilePeak


class WestDavarzan(IndexIranKhorasanRazavi, DayFilePeak):

    def __init__(self, **kwargs):
        super().__init__(T=0.12,
                         peak=3,
                         wheat_index_threshold=1110,
                         **kwargs)
