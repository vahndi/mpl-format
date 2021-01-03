from typing import Union

from matplotlib.axes import Axes

from mpl_format.compound_types import Color, FontSize
from mpl_format.styles import LINE_STYLE, get_line_style


class TicksFormatter(object):

    def __init__(self, axis: str, which: str, axes: Axes):
        """
        Create a new TicksFormatter.

        :param axis: One of {'x', 'y', 'both'}
        :param which: One of {'major', 'minor', 'both'}
        :param axes: Axes to operate on.
        """
        self._axis: str = axis
        self._which = which
        self._axes: Axes = axes

    def reset(self) -> 'TicksFormatter':
        """
        Set all parameters to defaults.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               reset=True)
        return self

    def set_direction(self, direction: str) -> 'TicksFormatter':
        """
        Puts ticks inside the axes, outside the axes, or both.

        :param direction: One of {'in', 'out', 'inout', 'in_out'}
        """
        direction = {
            'in': 'in',
            'out': 'out',
            'inout': 'inout',
            'in_out': 'inout'
        }[direction]
        self._axes.tick_params(axis=self._axis, which=self._which,
                               direction=direction)
        return self

    # region direction

    def set_direction_in(self) -> 'TicksFormatter':
        """
        Puts ticks inside the axes.
        """
        self.set_direction('in')
        return self

    def set_direction_out(self) -> 'TicksFormatter':
        """
        Puts ticks outside the axes.
        """
        self.set_direction('out')
        return self

    def set_direction_in_out(self) -> 'TicksFormatter':
        """
        Puts ticks inside and outside the axes.
        """
        self.set_direction('in_out')
        return self

    # endregion

    def set_length(self, length: float) -> 'TicksFormatter':
        """
        Set the tick length in points.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               length=length)
        return self

    def set_width(self, width: float) -> 'TicksFormatter':
        """
        Set the tick width in points.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               width=width)
        return self

    def set_color(self, color: Color) -> 'TicksFormatter':
        """
        Set the tick color.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               color=color)
        return self

    def set_padding(self, padding: float) -> 'TicksFormatter':
        """
        Set the distance in points between tick and label.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               pad=padding)
        return self

    def set_label_size(self, label_size: FontSize) -> 'TicksFormatter':
        """
        Set the tick label font size in points or as a string (e.g., 'large').
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               labelsize=label_size)
        return self

    def set_label_color(self, color: Color) -> 'TicksFormatter':
        """
        Set the tick label color.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               labelcolor=color)
        return self

    def set_colors(self, color: Color) -> 'TicksFormatter':
        """
        Set tick color and the label color to the same value.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               colors=color)
        return self

    def set_z_order(self, z_order: float) -> 'TicksFormatter':
        """
        Set the tick and label z-order.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               zorder=z_order)
        return self

    def show_top(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw ticks at the top of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               top=show)
        return self

    def show_bottom(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw ticks at the bottom of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               bottom=show)
        return self

    def show_left(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw ticks at the left of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               left=show)
        return self

    def show_right(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw ticks at the right of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               right=show)
        return self

    def show_top_labels(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw tick labels at the top of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               labeltop=show)
        return self

    def show_bottom_labels(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw tick labels at the bottom of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               labelbottom=show)
        return self

    def show_left_labels(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw tick labels at the left of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               labelleft=show)
        return self

    def show_right_labels(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw tick labels at the right of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               labelright=show)
        return self

    def set_label_rotation(self, rotation: float) -> 'TicksFormatter':
        """
        Set the tick label rotation.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               rotation=rotation)
        return self

    def set_grid_color(self, color: Color) -> 'TicksFormatter':
        """
        Set the grid line color.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               grid_color=color)
        return self

    def set_grid_alpha(self, alpha: float) -> 'TicksFormatter':
        """
        Set the transparency of grid lines: 0 (transparent) to 1 (opaque).
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               grid_alpha=alpha)
        return self

    def set_grid_line_width(self, line_width: float) -> 'TicksFormatter':
        """
        Set the width of grid lines in points.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               grid_linewidth=line_width)
        return self

    def set_grid_line_style(self, line_style: Union[str, LINE_STYLE]):
        """
        Set the line style of the grid lines.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               grid_linestyle=get_line_style(line_style))
        return self
