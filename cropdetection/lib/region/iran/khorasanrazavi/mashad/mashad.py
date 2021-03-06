from ..base import IndexIranKhorasanRazavi
from remotesensingmathematica.rs_mathematica import DayFilePeak


class Mashad(IndexIranKhorasanRazavi, DayFilePeak):

    def __init__(self, **kwargs):
        super().__init__(T=0.14,
                         peak=3,
                         wheat_index_threshold=900,
                         **kwargs)
