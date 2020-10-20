from ..base import HamedanBase


class WestHamedan(HamedanBase):

    def __init__(self, **kwargs):
        super().__init__(wheat_index_threshold=550, **kwargs)
