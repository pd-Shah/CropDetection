from ...base import IndexIranKhorasanRazavi
from remotesensingmathematica.rs_mathematica import DayFilePeak


class Khoshab(IndexIranKhorasanRazavi, DayFilePeak):

    def __init__(self, **kwargs):
        super().__init__(T=0.25,
                         peak=2,
                         wheat_index_threshold=950,
                         **kwargs)
