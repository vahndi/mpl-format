from typing import List, Union, Optional

from mpl_format.compound_types import Color
from mpl_format.animation.rate import Rate
from mpl_format.utils.color_utils import set_alpha, cross_fade


class ColorAnimation(object):

    def __init__(self,
                 colors: List[Color],
                 t: Optional[List[float]] = None,
                 rate: Optional[Union[Rate, str]] = None):

        self.colors: List[Color] = colors
        if t is not None:
            self.t: List[float] = t
        else:
            self.t = [0, 1]
        self.rate: Rate = (
            Rate.linear() if rate is None else
            rate if isinstance(rate, Rate) else
            Rate(rate)
        )

    @staticmethod
    def fade_in(color: Color) -> 'ColorAnimation':

        return ColorAnimation(
            colors=[set_alpha(color, 0), color],
            t=[0, 1]
        )

    def at(self, t: float) -> Color:

        for i in range(len(self.t)):
            if self.t[i + 1] >= t:
                return cross_fade(
                    from_color=self.colors[i],
                    to_color=self.colors[i + 1],
                    amount=(t - self.t[i]) / (self.t[i + 1] - self.t[i])
                )
