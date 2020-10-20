from ...base import HamedanBase


class EastRazan(HamedanBase):

    def __init__(self, **kwargs):
        super().__init__(wheat_index_threshold=800, **kwargs)
