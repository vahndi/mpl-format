from matplotlib.colors import to_rgba, ListedColormap
from numpy import linspace

from mpl_format.compound_types import Color
from mpl_format.utils.color_utils import cross_fade


class ColorMapGenerator(object):

    @staticmethod
    def fade_in_to_color(to_color: Color) -> ListedColormap:

        to_color = to_rgba(to_color)
        from_color = (to_color[0], to_color[1], to_color[2], 0.0)
        return ListedColormap(cross_fade(
            from_color, to_color, linspace(0, 1, 256)))

    @staticmethod
    def fade_from_white(to_color:  Color) -> ListedColormap:
        to_color = to_rgba(to_color)
        from_color = 'white'
        return ListedColormap(cross_fade(
            from_color, to_color, linspace(0, 1, 256)))
