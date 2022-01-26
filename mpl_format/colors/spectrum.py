from typing import List

from mpl_format.compound_types import Color


class Spectrum(object):

    colors: List[Color]

    def __getitem__(self, item: int):
        return self.colors[item]
