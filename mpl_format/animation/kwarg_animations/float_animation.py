from typing import List, Union, Optional

from mpl_format.animation.rate import Rate


class FloatAnimation(object):

    def __init__(self,
                 values: Optional[List[float]] = None,
                 t: Optional[List[float]] = None,
                 rate: Optional[Union[Rate, str]] = None):

        if values is not None:
            self.values: List[float] = values
        else:
            self.values = [0, 1]
        if t is not None:
            self.t: List[float] = t
        else:
            self.t = [0, 1]
        self.rate: Rate = (
            Rate.linear() if rate is None else
            rate if isinstance(rate, Rate) else
            Rate(rate)
        )

    def set_values(self, values: List[float]) -> 'FloatAnimation':

        self.values = values
        return self

    def reverse_values(self) -> 'FloatAnimation':

        return FloatAnimation(
            values=self.values[:: -1],
            t=self.t, rate=self.rate
        )

    @classmethod
    def linear(cls) -> 'FloatAnimation':
        return FloatAnimation(rate='linear')

    @classmethod
    def quadratic(cls) -> 'FloatAnimation':
        return FloatAnimation(rate='quadratic')

    @classmethod
    def cubic(cls) -> 'FloatAnimation':
        return FloatAnimation(rate='cubic')

    def at(self, t: float) -> float:

        for i in range(len(self.t)):
            if self.t[i + 1] >= t:
                dt = self.rate(
                    (t - self.t[i]) /
                    (self.t[i + 1] - self.t[i])
                )
                return (
                    self.values[i] +
                    (self.values[i + 1] - self.values[i]) * dt
                )

