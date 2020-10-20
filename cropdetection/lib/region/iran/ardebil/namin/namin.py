from ..base import ArdebilBase
from index.src.potato import PotatoV10


class Namin(ArdebilBase, PotatoV10):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
