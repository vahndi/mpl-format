from matplotlib.axes import Axes
from typing import Optional

from mpl_format.axes.axis_formatter import AxisFormatter
from mpl_format.axes.axis_utils import new_axes


class AxesFormatter(object):

    def __init__(self, axes: Axes):
        """
        Create a new AxesFormatter

        :param axes: The matplotlib Axes instance to wrap.
        """
        self._axes: Axes = axes

    @staticmethod
    def new(width: int, height: int) -> 'AxesFormatter':
        """
        Create a new Axes and return it wrapped in an AxesFormatter

        :param width: Width for the new axes.
        :param height: Height for the new axes.
        """
        axes = new_axes(width=width, height=height)
        return AxesFormatter(axes)

    @property
    def axes(self) -> Axes:
        """
        Return the wrapped Axes instance.
        """
        return self._axes

    @property
    def x_axis(self) -> AxisFormatter:
        """
        Return an AxisFormatter for the x-axis of the wrapped Axes.
        """
        return AxisFormatter(self._axes.xaxis)

    @property
    def y_axis(self) -> AxisFormatter:
        """
        Return an AxisFormatter for the y-axis of the wrapped Axes.
        """
        return AxisFormatter(self._axes.yaxis)

    def set_title_size(self, font_size: int) -> 'AxesFormatter':
        """
        Set the font size for the title of the wrapped Axes.
        """
        self._axes.set_title(self._axes.get_title(), fontsize=font_size)
        return self

    def set_x_label_size(self, font_size: int) -> 'AxesFormatter':
        """
        Set the font size for the x-axis label.
        """
        self.x_axis.set_label_size(font_size)
        return self

    def set_y_label_size(self, font_size: int) -> 'AxesFormatter':
        """
        Set the font size for the x-axis label.
        """
        self.y_axis.set_label_size(font_size)
        return self

    def set_tick_label_sizes(self, font_size: int) -> 'AxesFormatter':
        """
        Set the font size for the tick labels of the wrapped Axes.
        """
        self.x_axis.set_label_size(font_size)
        self.y_axis.set_label_size(font_size)
        return self

    def set_font_sizes(
            self,
            title: Optional[int] = None,
            axis_labels: Optional[int] = None,
            x_axis_label: Optional[int] = None, y_axis_label: Optional[int] = None,
            tick_labels: Optional[int] = None,
            x_tick_labels: Optional[int] = None, y_tick_labels: Optional[int] = None,
            legend: Optional[int] = None,
            figure_title: Optional[int] = None
    ) -> 'AxesFormatter':

        ax = self._axes
        if title is not None:
            self.set_title_size(title)
        if axis_labels is not None:
            self.x_axis.set_label_size(axis_labels)
            self.y_axis.set_label_size(axis_labels)
        if x_axis_label is not None:
            self.x_axis.set_label_size(x_axis_label)
        if y_axis_label is not None:
            self.y_axis.set_label_size(y_axis_label)
        if tick_labels is not None:
            self.set_tick_label_sizes(tick_labels)
        if x_tick_labels is not None:
            self.x_axis.set_tick_label_size(x_tick_labels)
        if y_tick_labels is not None:
            self.y_axis.set_tick_label_size(y_tick_labels)
            ax.tick_params(axis='y', labelsize=y_tick_labels)
        if legend is not None:
            ax.legend(fontsize=legend)
        if figure_title is not None:
            ax.set_title(ax.get_title(), fontsize=title)

        return self
