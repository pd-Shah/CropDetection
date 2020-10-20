from ...base import HamedanBase


class NorthKabodAhang(HamedanBase):

    def __init__(self, **kwargs):
        super().__init__(wheat_index_threshold=500, **kwargs)
