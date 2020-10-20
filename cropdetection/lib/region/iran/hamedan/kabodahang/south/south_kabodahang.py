from ...base import HamedanBase


class SouthKabodAhang(HamedanBase):

    def __init__(self, **kwargs):
        super().__init__(wheat_index_threshold=500, **kwargs)
