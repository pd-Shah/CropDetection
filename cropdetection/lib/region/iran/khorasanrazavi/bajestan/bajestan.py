from ..base import KhorasanRazaviBase
from remotesensingmathematica.rs_mathematica import DayFilePeak


class Bajestan(KhorasanRazaviBase, DayFilePeak):

    def __init__(self, **kwargs):
        super().__init__(T=0.12, peak=3, **kwargs)
