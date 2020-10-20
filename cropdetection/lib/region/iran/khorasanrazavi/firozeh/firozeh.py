from ..base import KhorasanRazaviBase
from cropdetection.lib.remotesensingmathematica.rs_mathematica import DayFilePeak


class Firozeh(KhorasanRazaviBase, DayFilePeak):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
