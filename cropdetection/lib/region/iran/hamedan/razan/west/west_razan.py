from ...base import HamedanBase


class WestRazan(HamedanBase):

    def __init__(self, **kwargs):
        super().__init__(wheat_index_threshold=850, **kwargs)
