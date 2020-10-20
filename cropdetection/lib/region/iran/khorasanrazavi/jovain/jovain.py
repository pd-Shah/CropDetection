from ..base import KhorasanRazaviBase
from cropdetection.lib.remotesensingmathematica.rs_mathematica import DayFilePeak


class Jovain(KhorasanRazaviBase, DayFilePeak):

    def __init__(self, **kwargs):
        super().__init__(T=0.15,
                         peak=2,
                         wheat_index_threshold=1050,
                         **kwargs)
