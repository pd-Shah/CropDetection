from ..base import HamedanBase


class EastHamedan(HamedanBase):

    def __init__(self, **kwargs):
        super().__init__(wheat_index_threshold=480, **kwargs)
