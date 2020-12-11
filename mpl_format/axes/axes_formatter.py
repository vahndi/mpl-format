from math import pi
from typing import Optional, Union, List, Tuple, Iterable

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle, RegularPolygon, Circle, Arc, Arrow, \
    Ellipse, FancyArrow, Patch, FancyArrowPatch, FancyBboxPatch, Polygon, Wedge, \
    BoxStyle
from matplotlib.path import Path
from numpy import ndarray, linspace
from pandas import DataFrame, Series
from scipy.interpolate import interp1d

from compound_types.arrays import ArrayLike
from compound_types.built_ins import FloatOrFloatIterable, StrOrStrIterable, \
    DictOrDictIterable, BoolOrBoolIterable, FloatIterable
from mpl_format.axes.axis_formatter import AxisFormatter
from mpl_format.axes.axis_utils import new_axes
from mpl_format.compound_types import FontSize, Color, LegendLocation, \
    StringMapper, ColorOrColorIterable
from mpl_format.legend.legend_formatter import LegendFormatter
from mpl_format.patches.patch_list_formatter import PatchListFormatter
from mpl_format.styles import LINE_STYLE, CAP_STYLE, JOIN_STYLE, ARROW_STYLE, \
    CONNECTION_STYLE, DRAW_STYLE, MARKER_STYLE
from mpl_format.text.text_formatter import TextFormatter
from mpl_format.text.text_utils import wrap_text
from mpl_format.utils.arg_checks import check_h_align
from mpl_format.utils.color_utils import cross_fade
from mpl_format.utils.io_utils import save_plot


class AxesFormatter(object):

    def __init__(self, axes: Optional[Axes] = None,
                 width: Optional[int] = None, height: Optional[int] = None,
                 constrained_layout: bool = False):
        """
        Create a new AxesFormatter

        :param axes: The matplotlib Axes instance to wrap.
        :param width: Width of new Axes, if none are given.
        :param height: Height of new Axes, if none are given.
        :param constrained_layout: Option for constrained_layout of new Axes.
        """
        if axes is None:
            self._axes: Axes = new_axes(
                width=width, height=height,
                constrained_layout=constrained_layout
            )
        else:
            self._axes: Axes = axes
        self._x_axis: AxisFormatter = AxisFormatter(self._axes.xaxis)
        self._y_axis: AxisFormatter = AxisFormatter(self._axes.yaxis)
        self._title: TextFormatter = TextFormatter(self._axes.title)
        legend = self._axes.get_legend()
        if legend is None:
            self._legend = None
        else:
            self._legend = LegendFormatter(legend)

    # region properties

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
        return self._x_axis

    @property
    def y_axis(self) -> AxisFormatter:
        """
        Return an AxisFormatter for the y-axis of the wrapped Axes.
        """
        return self._y_axis

    @property
    def legend(self) -> LegendFormatter:
        """
        Return a LegendFormatter for the legend of the wrapped Axes,
        if there is one.
        """
        return self._legend

    @property
    def title(self) -> TextFormatter:
        return self._title

    # endregion

    # region set text

    def set_title_text(self, text: str) -> 'AxesFormatter':
        """
        Set the text of the Axes title.

        :param text: The text to use for the Axes title.
        """
        self.title.set_text(text)
        return self

    def map_title_text(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the label text for the title using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.title.map(mapping=mapping)
        return self

    def set_x_label_text(self, text: str) -> 'AxesFormatter':
        """
        Set the text for the x-axis label.

        :param text: The text to use for the Axis label.
        """
        self.x_axis.set_label_text(text)
        return self

    def set_y_label_text(self, text: str) -> 'AxesFormatter':
        """
        Set the text for the y-axis label.

        :param text: The text to use for the Axis label.
        """
        self.y_axis.set_label_text(text)
        return self

    def set_text(self, title: Optional[str] = None,
                 x_label: Optional[str] = None,
                 y_label: Optional[str] = None) -> 'AxesFormatter':
        """
        Set text properties for elements of the Axes.

        :param title: Text for the title.
        :param x_label: Text for the x-axis label.
        :param y_label: Text for the y-axis label.
        """
        if title is not None:
            self.set_title_text(title)
        if x_label is not None:
            self.x_axis.set_label_text(x_label)
        if y_label is not None:
            self.y_axis.set_label_text(y_label)
        return self

    # endregion

    # region wrap text

    def wrap_title(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for the title if it exceeds a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self.set_title_text(wrap_text(self.title.text, max_width=max_width))
        return self

    def wrap_x_label(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for the x-axis label if it exceeds a given width of
        characters.

        :param max_width: The maximum character width per line.
        """
        self.x_axis.wrap_label(max_width=max_width)
        return self

    def wrap_y_label(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for the y-axis label if it exceeds a given width of
        characters.

        :param max_width: The maximum character width per line.
        """
        self.y_axis.wrap_label(max_width=max_width)
        return self

    def wrap_axis_labels(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the texts for the x and y-axis labels if they exceeds a given width
        of characters.

        :param max_width: The maximum character width per line.
        """
        self.wrap_x_label(max_width=max_width)
        self.wrap_y_label(max_width=max_width)
        return self

    def wrap_x_tick_labels(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for each tick label on the x-axis with new lines if it
        exceeds a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self.x_axis.wrap_tick_labels(max_width=max_width)
        return self

    def wrap_y_tick_labels(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for each tick label on the y-axes with new lines if it
        exceeds a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self.y_axis.wrap_tick_labels(max_width=max_width)
        return self

    def wrap_tick_labels(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for each tick label on each axis with new lines if it
        exceeds a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self.wrap_x_tick_labels(max_width=max_width)
        self.wrap_y_tick_labels(max_width=max_width)
        return self

    # endregion

    # region set font sizes

    def set_title_size(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the title of the wrapped Axes.

        :param font_size: Size of the font in points, or size name.
        """
        self.title.set_size(font_size)
        return self

    def set_x_label_size(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the x-axis label.

        :param font_size: Size of the font in points, or size name.
        """
        self.x_axis.set_label_size(font_size)
        return self

    def set_y_label_size(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the x-axis label.

        :param font_size: Size of the font in points, or size name.
        """
        self.y_axis.set_label_size(font_size)
        return self

    def set_axis_label_sizes(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the axis labels.

        :param font_size: Size of the font in points, or size name.
        """
        self.set_x_label_size(font_size)
        self.set_y_label_size(font_size)
        return self

    def set_x_tick_label_size(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the x-axis tick labels.

        :param font_size: Size of the font in points, or size name.
        """
        self.x_axis.set_tick_label_size(font_size)
        return self

    def set_y_tick_label_size(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the y-axis tick labels.

        :param font_size: Size of the font in points, or size name.
        """
        self.y_axis.set_tick_label_size(font_size)
        return self

    def set_tick_label_sizes(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the tick labels of the wrapped Axes.

        :param font_size: Size of the font in points, or size name.
        """
        self.set_x_tick_label_size(font_size)
        self.set_y_tick_label_size(font_size)
        return self

    def set_font_sizes(
            self,
            title: Optional[int] = None,
            axis_labels: Optional[int] = None,
            x_axis_label: Optional[int] = None,
            y_axis_label: Optional[int] = None,
            tick_labels: Optional[int] = None,
            x_tick_labels: Optional[int] = None,
            y_tick_labels: Optional[int] = None,
            legend: Optional[int] = None,
            figure_title: Optional[int] = None
    ) -> 'AxesFormatter':
        """
        Set font sizes for different axes elements.
        """
        ax = self._axes
        if title is not None:
            self.set_title_size(title)
        if axis_labels is not None:
            self.set_axis_label_sizes(axis_labels)
        if x_axis_label is not None:
            self.set_x_label_size(x_axis_label)
        if y_axis_label is not None:
            self.set_y_label_size(y_axis_label)
        if tick_labels is not None:
            self.set_tick_label_sizes(tick_labels)
        if x_tick_labels is not None:
            self.set_x_tick_label_size(x_tick_labels)
        if y_tick_labels is not None:
            self.set_y_label_size(y_tick_labels)
        if legend is not None:
            ax.legend(fontsize=legend)
        if figure_title is not None:
            ax.figure.suptitle(ax.get_title(), fontsize=figure_title)

        return self

    # endregion

    # region map labels

    def map_x_axis_label(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the label text for the x-axis using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.x_axis.map_label_text(mapping)
        return self

    def map_y_axis_label(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the label text for the y-axis using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.y_axis.map_label_text(mapping)
        return self

    def map_axis_labels(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the label text for the x and y axes using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.map_x_axis_label(mapping)
        self.map_y_axis_label(mapping)
        return self

    def map_x_tick_labels(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the tick label text for the x-axis using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.x_axis.map_tick_label_text(mapping)
        return self

    def map_y_tick_labels(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the tick label text for the y-axis using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.y_axis.map_tick_label_text(mapping)
        return self

    def map_tick_labels(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the tick label text using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.map_x_tick_labels(mapping)
        self.map_y_tick_labels(mapping)
        return self

    # endregion

    # region remove

    def remove_title(self) -> 'AxesFormatter':
        """
        Remove the title from the Axes.
        """
        self.set_title_text('')
        return self

    def remove_legend(self) -> 'AxesFormatter':
        """
        Remove the legend from the Axes.
        """
        legend = self._axes.get_legend()
        if legend is not None:
            legend.remove()
            self._legend = None
        return self

    def remove_x_ticks(self) -> 'AxesFormatter':
        """
        Remove x-ticks from the Axes.
        """
        self._axes.set_xticks([])
        return self

    def remove_y_ticks(self) -> 'AxesFormatter':
        """
        Remove y-ticks from the Axes.
        """
        self._axes.set_yticks([])
        return self

    def remove_axes_ticks(self) -> 'AxesFormatter':
        """
        Remove x- and y- ticks from the Axes.
        """
        self.remove_x_ticks()
        self.remove_y_ticks()
        return self

    def remove_x_label(self) -> 'AxesFormatter':
        """
        Remove the label from the x-axis.
        """
        self.x_axis.remove_label()
        return self

    def remove_y_label(self) -> 'AxesFormatter':
        """
        Remove the label from the y-axis.
        """
        self.y_axis.remove_label()
        return self

    def remove_axes_labels(self) -> 'AxesFormatter':
        """
        Remove the labels from the x- and y- axes.
        """
        self.remove_x_label()
        self.remove_y_label()
        return self

    # endregion

    # region rotation

    def rotate_x_label(self,
                       rotation: int,
                       how: str = 'absolute') -> 'AxesFormatter':
        """
        Set the rotation of the x-axis label.

        :param rotation: The rotation value to set in degrees.
        :param how: 'absolute' or 'relative'
        """
        self.x_axis.rotate_label(rotation, how)
        return self

    def rotate_y_label(self,
                       rotation: int,
                       how: str = 'absolute') -> 'AxesFormatter':
        """
        Set the rotation of the x-axis label.

        :param rotation: The rotation value to set in degrees.
        :param how: 'absolute' or 'relative'
        """
        self.y_axis.rotate_label(rotation, how)
        return self

    def rotate_x_tick_labels(self,
                             rotation: int,
                             how: str = 'absolute') -> 'AxesFormatter':
        """
        Set the rotation of the x-axis tick labels.

        :param rotation: The rotation value to set in degrees.
        :param how: 'absolute' or 'relative'
        """
        self.x_axis.rotate_tick_labels(rotation=rotation, how=how)
        return self

    def rotate_y_tick_labels(self,
                             rotation: int,
                             how: str = 'absolute') -> 'AxesFormatter':
        """
        Set the rotation of the y-axis tick labels.

        :param rotation: The rotation value to set in degrees.
        :param how: 'absolute' or 'relative'
        """
        self.y_axis.rotate_tick_labels(rotation=rotation, how=how)
        return self

    # endregion

    # region spans

    def add_h_line(self, y: Union[float, str] = 0,
                   x_min: Union[float, str] = 0,
                   x_max: Union[float, str] = 1,
                   color: Optional[Color] = None,
                   alpha: Optional[float] = None,
                   line_style: Optional[str] = None,
                   line_width: Optional[float] = None,
                   marker_edge_color: Optional[Color] = None,
                   marker_edge_width: Optional[Color] = None,
                   marker_face_color: Optional[Color] = None,
                   marker_size: Optional[float] = None) -> 'AxesFormatter':
        """
        Add a horizontal line to the plot.

        :param y: y position in data coordinates of the horizontal line
        :param x_min: Between 0 and 1, 0 being the far left of the plot,
                      1 the far right of the plot
        :param x_max: Between 0 and 1, 0 being the far left of the plot,
                      1 the far right of the plot
        :param color: Color of the line
        :param alpha: Opacity of the line
        :param line_style: One of {'-', '--', '-.', ':', ''}
        :param line_width: Width of the line
        :param marker_edge_color: Color for the edges of the line markers
        :param marker_edge_width: Width for the edges of the line markers
        :param marker_face_color: Color for the markers
        :param marker_size: Size of the markers.
        """
        kwargs = {}
        for arg, mpl_arg in zip(
            [color, line_style, line_width,
             marker_edge_color, marker_edge_width,
             marker_face_color, marker_size,
             alpha],
            ['c', 'ls', 'lw', 'mec', 'mew', 'mfc', 'ms', 'alpha']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg

        self._axes.axhline(
            y=y, xmin=x_min, xmax=x_max,
            **kwargs
        )
        return self

    def add_v_line(self, x: Union[float, str] = 0,
                   y_min: Union[float, str] = 0,
                   y_max: Union[float, str] = 1,
                   color: Optional[Color] = None, alpha: Optional[float] = None,
                   line_style: Optional[str] = None,
                   line_width: Optional[float] = None,
                   marker_edge_color: Optional[Color] = None,
                   marker_edge_width: Optional[Color] = None,
                   marker_face_color: Optional[Color] = None,
                   marker_size: Optional[float] = None) -> 'AxesFormatter':
        """
        Add a vertical line to the plot.

        :param x: x position in data coordinates of the vertical line
        :param y_min: Should be between 0 and 1, with 0 being the bottom of the
                      plot, and 1 the top of the plot
        :param y_max: Should be between 0 and 1, with 0 being the bottom of the
                      plot, and 1 the top of the plot
        :param color: Color of the line
        :param alpha: Opacity of the line
        :param line_style: One of {'-', '--', '-.', ':', ''}
        :param line_width: Width of the line
        :param marker_edge_color: Color for the edges of the line markers
        :param marker_edge_width: Width for the edges of the line markers
        :param marker_face_color: Color for the markers
        :param marker_size: Size of the markers.
        """
        kwargs = {}
        for arg, mpl_arg in zip(
            [color, line_style, line_width, marker_edge_color,
             marker_edge_width, marker_face_color, marker_size, alpha],
            ['c', 'ls', 'lw', 'mec', 'mew', 'mfc', 'ms', 'alpha']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg

        self._axes.axvline(
            x=x, ymin=y_min, ymax=y_max,
            **kwargs
        )
        return self

    def add_h_lines(self, y: FloatOrFloatIterable,
                    x_min: FloatOrFloatIterable,
                    x_max: FloatOrFloatIterable,
                    colors='k', line_styles: str = 'solid',
                    label: Optional[str] = '') -> 'AxesFormatter':
        """
        Plot horizontal lines at each y from x_min to x_max.

        :param y: x-indexes where to plot the lines.
        :param x_min: Beginning of each or all lines.
        :param x_max: End of each or all lines.
        :param colors: Line colors.
        :param line_styles: One of {'solid', 'dashed', 'dashdot', 'dotted'}
        :param label: Label.
        """
        self._axes.hlines(y=y, xmin=x_min, xmax=x_max,
                          colors=colors, linestyles=line_styles,
                          label=label)
        return self

    def add_v_lines(self, x: FloatOrFloatIterable,
                    y_min: FloatOrFloatIterable,
                    y_max: FloatOrFloatIterable,
                    colors='k', line_styles: str = 'solid',
                    label: Optional[str] = '') -> 'AxesFormatter':
        """
        Plot vertical lines at each x from y_min to y_max.

        :param x: x-indexes where to plot the lines.
        :param y_min: Beginning of each or all lines.
        :param y_max: End of each or all lines.
        :param colors: Line colors.
        :param line_styles: One of {'solid', 'dashed', 'dashdot', 'dotted'}
        :param label: Label.
        """
        self._axes.vlines(x=x, ymin=y_min, ymax=y_max,
                          colors=colors, linestyles=line_styles,
                          label=label)
        return self

    def fill_between(self, x: Union[ArrayLike, str],
                     y1: Union[float, ArrayLike, str],
                     y2: Union[float, ArrayLike, str],
                     data: Optional[DataFrame] = None,
                     where: Optional[ArrayLike] = None,
                     interpolate: bool = False,
                     step: Optional[str] = None,
                     color: Optional[Color] = None,
                     alpha: Optional[float] = None,
                     line_style: Optional[str] = None,
                     line_width: Optional[float] = None,
                     edge_color: Optional[Color] = None,
                     face_color: Optional[Color] = None) -> 'AxesFormatter':
        """
        Make filled polygons between two curves.

        :param x: N-length array of, or name of column with the x data.
        :param y1: N-length array, scalar, or name of column with the y1 data.
        :param y2: N-length array, scalar, or name of column with the y2 data.
        :param data: Optional DataFrame with x, y1 and y2 columns.
        :param where: If None, default to fill between everywhere. If not None,
                      it is an N-length numpy boolean array and the fill will
                      only happen over the regions where where==True.
        :param interpolate: If True, interpolate between the two lines to find
                            the precise point of intersection. Otherwise, the
                            start and end points of the filled region will only
                            occur on explicit values in the x array.
        :param step: One of {‘pre’, ‘post’, ‘mid’}. If not None, fill with step
                     logic.
        :param color: matplotlib color arg or sequence of rgba tuples
        :param alpha: Opacity.
        :param line_style: One of {'-', '--', '-.', ':', ''}
        :param line_width: float or sequence of floats
        :param edge_color: matplotlib color spec or sequence of specs
        :param face_color: matplotlib color spec or sequence of specs
        """
        # get arrays from DataFrame
        if data is not None:
            if isinstance(x, str):
                x = data[x]
            if isinstance(y1, str):
                y1 = data[y1]
            if isinstance(y2, str):
                y2 = data[y2]
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [color, alpha, line_style, line_width, edge_color, face_color],
            ['color', 'alpha', 'line_style',
             'line_width', 'edge_color', 'face_color']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        # call matplotlib method
        self._axes.fill_between(
            x=x, y1=y1, y2=y2,
            where=where, interpolate=interpolate,
            step=step,
            **kwargs
        )
        return self

    # endregion

    # region colors

    def set_face_color(self, color: Color) -> 'AxesFormatter':

        self._axes.set_facecolor(color)
        return self

    def get_frame_color(self) -> Union[Color, List[Color]]:
        """
        Return the color of the frame if all edges are the same color,
        otherwise a list of the top, bottom, left and right colors.
        """
        colors = self.get_frame_colors()
        if len(set(colors)) == 1:
            return colors[0]
        else:
            return self.get_frame_colors()

    def set_frame_color(self, color: Color) -> 'AxesFormatter':

        for pos in ['top', 'bottom', 'left', 'right']:
            self._axes.spines[pos].set_edgecolor(color)
        return self

    def get_frame_colors(self) -> List[Color]:
        """
        Return the colors of the top, bottom, left and right edges of the Axes.
        """
        return [
            self._axes.spines[pos].get_edgecolor()
            for pos in ['top', 'bottom', 'left', 'right']
        ]

    def set_tick_color(self, color: Color) -> 'AxesFormatter':

        self.x_axis.set_tick_color(color=color)
        self.y_axis.set_tick_color(color=color)
        return self

    # endregion

    # region shapes

    # region patches

    def add_text(
            self, x: FloatOrFloatIterable,
            y: FloatOrFloatIterable,
            text: StrOrStrIterable,
            font_dict: Optional[DictOrDictIterable] = None,
            **kwargs
    ) -> 'AxesFormatter':
        """
        Add a single or multiple text blocks to the plot.

        :param x: x-coordinate(s) of the text.
        :param y: y-coordinate(s) of the text.
        :param text: String or iterable of text strings to add.
        :param font_dict: A dictionary to override the default text properties.
                          If font_dict is None, the defaults are determined by
                          your rc parameters.
        :param kwargs: Other miscellaneous Text parameters.
        """
        if isinstance(x, Iterable) or isinstance(y, Iterable):
            if not isinstance(x, Iterable):
                x = [x] * len(y)
            elif not isinstance(y, Iterable):
                y = [y] * len(x)
        else:
            x = [x]
            y = [y]
            if isinstance(text, str):
                text = [text] * len(x)
            if type(font_dict) in (type(None), dict):
                font_dict = [font_dict] * len(x)

        for x_i, y_i, text_i, font_dict_i in zip(x, y, text, font_dict):
            self._axes.text(
                x=x_i, y=y_i, s=text_i,
                fontdict=font_dict_i, **kwargs
            )
        return self

    def add_arc(
            self, x: float, y: float, width: float, height: float,
            angle: float = 0.0,
            theta_start: float = 0.0, theta_end: float = 360.0,
            alpha: Optional[float] = None,
            cap_style: Optional[Union[str, CAP_STYLE]] = None,
            color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            face_color: Optional[Color] = None,
            fill: bool = True,
            join_style: Optional[Union[str, JOIN_STYLE]] = None,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[float] = None
    ):
        """
        Add an elliptical arc, i.e. a segment of an ellipse.

        :param x: The x-coordinate of the center of the ellipse.
        :param y: The y-coordinate of the center of the ellipse.
        :param width: The length of the horizontal axis.
        :param height: The length of the vertical axis.
        :param angle: Rotation of the ellipse in degrees (counterclockwise).
        :param theta_start: Starting angle of the arc in degrees.
                            Relative to angle, e.g. if angle = 45 and
                            theta_start = 90 the absolute starting angle is 135.
        :param theta_end: Ending angle of the arc in degrees.
        :param alpha: Opacity.
        :param cap_style: Cap style.
        :param color: Use to set both the edge-color and the face-color.
        :param edge_color: Edge color.
        :param face_color: Face color.
        :param fill: Whether to fill the rectangle.
        :param join_style: Join style.
        :param label: Label for the object in the legend.
        :param line_style: Line style for edge.
        :param line_width: Line width for edge.
        """
        if line_style and isinstance(line_style, LINE_STYLE):
            line_style = line_style.name
        if cap_style and isinstance(cap_style, CAP_STYLE):
            cap_style = cap_style.name
        if join_style and isinstance(join_style, JOIN_STYLE):
            join_style = join_style.name
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [alpha, cap_style, color, edge_color, face_color,
             fill, join_style, label, line_style, line_width],
            ['alpha', 'capstyle', 'color', 'edgecolor', 'facecolor',
             'fill', 'joinstyle', 'label', 'linestyle', 'linewidth']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        arc = Arc(
            xy=(x, y), width=width, height=height,
             angle=angle, theta1=theta_start, theta2=theta_end,
            **kwargs
        )
        self._axes.add_artist(arc)
        return self

    def add_arrow(
            self, x: float, y: float, dx: float, dy: float,
            width: float = 1.0,
            alpha: Optional[float] = None,
            cap_style: Optional[Union[str, CAP_STYLE]] = None,
            color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            face_color: Optional[Color] = None,
            fill: bool = True,
            join_style: Optional[Union[str, JOIN_STYLE]] = None,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[float] = None
    ):
        """
        Add an an arrow patch.

        :param x: The x-coordinate of the arrow tail.
        :param y: The y-coordinate of the arrow tail.
        :param dx: Arrow length in the x direction.
        :param dy: Arrow length in the y direction.
        :param width: Scale factor for the width of the arrow.
                      With a default value of 1, the tail width is 0.2 and
                      head width is 0.6.
        :param alpha: Opacity.
        :param cap_style: Cap style.
        :param color: Use to set both the edge-color and the face-color.
        :param edge_color: Edge color.
        :param face_color: Face color.
        :param fill: Whether to fill the rectangle.
        :param join_style: Join style.
        :param label: Label for the object in the legend.
        :param line_style: Line style for edge.
        :param line_width: Line width for edge.
        """
        if line_style and isinstance(line_style, LINE_STYLE):
            line_style = line_style.name
        if cap_style and isinstance(cap_style, CAP_STYLE):
            cap_style = cap_style.name
        if join_style and isinstance(join_style, JOIN_STYLE):
            join_style = join_style.name
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [alpha, cap_style, color, edge_color, face_color,
             fill, join_style, label, line_style, line_width],
            ['alpha', 'capstyle', 'color', 'edgecolor', 'facecolor',
             'fill', 'joinstyle', 'label', 'linestyle', 'linewidth']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        arrow = Arrow(
            x=x, y=y, dx=dx, dy=dy, width=width,
            **kwargs
        )
        self._axes.add_artist(arrow)
        return self

    def add_circle(
            self, x: float, y: float,
            radius: float,
            alpha: Optional[float] = None,
            cap_style: Optional[Union[str, CAP_STYLE]] = None,
            color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            face_color: Optional[Color] = None,
            fill: bool = True,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[float] = None,
            join_style: Optional[Union[str, JOIN_STYLE]] = None
    ) -> 'AxesFormatter':
        """
        Add a rectangle to the Axes.

        :param x: The left rectangle coordinate.
        :param y: The bottom rectangle coordinate.
        :param radius: The radius of the circle.
        :param alpha: Opacity.
        :param color: Use to set both the edge-color and the face-color.
        :param edge_color: Edge color.
        :param face_color: Face color.
        :param fill: Whether to fill the rectangle.
        :param join_style: Join style.
        :param label: Label for the object in the legend.
        :param line_style: Line style for edge.
        :param line_width: Line width for edge.
        :param cap_style: Cap style.
        """
        if line_style and isinstance(line_style, LINE_STYLE):
            line_style = line_style.name
        if cap_style and isinstance(cap_style, CAP_STYLE):
            cap_style = cap_style.name
        if join_style and isinstance(join_style, JOIN_STYLE):
            join_style = join_style.name
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [alpha, cap_style, color, edge_color, face_color,
             fill, join_style, label, line_style, line_width],
            ['alpha', 'capstyle', 'color', 'edgecolor', 'facecolor',
             'fill', 'joinstyle', 'label', 'linestyle', 'linewidth']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        polygon = Circle(
            xy=(x, y), radius=radius,
            **kwargs
        )
        self._axes.add_artist(polygon)
        return self

    def add_ellipse(
            self, x: float, y: float, width: float, height: float,
            angle: float = 0.0,
            alpha: Optional[float] = None,
            cap_style: Optional[Union[str, CAP_STYLE]] = None,
            color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            face_color: Optional[Color] = None,
            fill: bool = True,
            join_style: Optional[Union[str, JOIN_STYLE]] = None,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[float] = None
    ):
        """
        Add an elliptical arc, i.e. a segment of an ellipse.

        :param x: The x-coordinate of the center of the ellipse.
        :param y: The y-coordinate of the center of the ellipse.
        :param width: The length (diameter) of the horizontal axis.
        :param height: The length (diameter) of the vertical axis.
        :param angle: Rotation of the ellipse in degrees (counterclockwise).
        :param alpha: Opacity.
        :param cap_style: Cap style.
        :param color: Use to set both the edge-color and the face-color.
        :param edge_color: Edge color.
        :param face_color: Face color.
        :param fill: Whether to fill the rectangle.
        :param join_style: Join style.
        :param label: Label for the object in the legend.
        :param line_style: Line style for edge.
        :param line_width: Line width for edge.
        """
        if line_style and isinstance(line_style, LINE_STYLE):
            line_style = line_style.name
        if cap_style and isinstance(cap_style, CAP_STYLE):
            cap_style = cap_style.name
        if join_style and isinstance(join_style, JOIN_STYLE):
            join_style = join_style.name
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [alpha, cap_style, color, edge_color, face_color,
             fill, join_style, label, line_style, line_width],
            ['alpha', 'capstyle', 'color', 'edgecolor', 'facecolor',
             'fill', 'joinstyle', 'label', 'linestyle', 'linewidth']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        ellipse = Ellipse(
            xy=(x, y), width=width, height=height, angle=angle,
            **kwargs
        )
        self._axes.add_artist(ellipse)
        return self

    def add_fancy_arrow(
            self, x: float, y: float, dx: float, dy: float,
            width: float = 0.001,
            length_includes_head: bool = False,
            head_width: Optional[float] = None,
            head_length: Optional[float] = None,
            shape: str = 'full',
            overhang: float = 0.0,
            head_starts_at_zero: bool = False,
            alpha: Optional[float] = None,
            cap_style: Optional[Union[str, CAP_STYLE]] = None,
            color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            face_color: Optional[Color] = None,
            fill: bool = True,
            join_style: Optional[Union[str, JOIN_STYLE]] = None,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[float] = None
    ):
        """
        Like Arrow, but lets you set head width and head height independently.

        :param x: The x-coordinate of the arrow tail.
        :param y: The y-coordinate of the arrow tail.
        :param dx: Arrow length in the x direction.
        :param dy: Arrow length in the y direction.
        :param width: Width of full arrow tail.
        :param length_includes_head: True if head is to be counted in
                                     calculating the length.
        :param head_width: Total width of the full arrow head
        :param head_length: Length of arrow head
        :param shape: Draw the left-half, right-half, or full arrow.
                      One of ['full', 'left', 'right'].
        :param overhang: Fraction that the arrow is swept back
                         (0 overhang means triangular shape).
                         Can be negative or greater than one.
        :param head_starts_at_zero: If True, the head starts being drawn at
                                    coordinate 0 instead of ending at
                                    coordinate 0.
        :param alpha: Opacity.
        :param cap_style: Cap style.
        :param color: Use to set both the edge-color and the face-color.
        :param edge_color: Edge color.
        :param face_color: Face color.
        :param fill: Whether to fill the rectangle.
        :param join_style: Join style.
        :param label: Label for the object in the legend.
        :param line_style: Line style for edge.
        :param line_width: Line width for edge.
        """
        if line_style and isinstance(line_style, LINE_STYLE):
            line_style = line_style.name
        if cap_style and isinstance(cap_style, CAP_STYLE):
            cap_style = cap_style.name
        if join_style and isinstance(join_style, JOIN_STYLE):
            join_style = join_style.name
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [alpha, cap_style, color, edge_color, face_color,
             fill, join_style, label, line_style, line_width],
            ['alpha', 'capstyle', 'color', 'edgecolor', 'facecolor',
             'fill', 'joinstyle', 'label', 'linestyle', 'linewidth']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        arrow = FancyArrow(
            x=x, y=y, dx=dx, dy=dy, width=width,
            length_includes_head=length_includes_head,
            head_width=head_width,
            head_length=head_length,
            shape=shape,
            overhang=overhang,
            head_starts_at_zero=head_starts_at_zero,
            **kwargs
        )
        self._axes.add_artist(arrow)
        return self

    def add_fancy_arrow_patch(
            self, x: float, y: float, dx: float, dy: float,
            path: Optional[Path] = None,
            arrow_style: Union[str, ARROW_STYLE] = 'simple',
            connection_style: Union[str, CONNECTION_STYLE] = 'arc3',
            tail_patch: Optional[Patch] = None,
            head_patch: Optional[Patch] = None,
            tail_shrink_factor: Optional[float] = 2,
            head_shrink_factor: Optional[float] = 2,
            mutation_scale: Optional[float] = 1,
            mutation_aspect: Optional[float] = None,
            dpi_cor: Optional[float] = 1,
            alpha: Optional[float] = None,
            cap_style: Optional[Union[str, CAP_STYLE]] = None,
            color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            face_color: Optional[Color] = None,
            fill: bool = True,
            join_style: Optional[Union[str, JOIN_STYLE]] = None,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[float] = None
    ):
        """
        Like Arrow, but lets you set head width and head height independently.

        :param x: The x-coordinate of the arrow tail.
        :param y: The y-coordinate of the arrow tail.
        :param dx: Arrow length in the x direction.
        :param dy: Arrow length in the y direction.
        :param path: If provided, an arrow is drawn along this path and
                     tail_patch, head_patch, tail_shrink_factor, and
                     head_shrink_factor are ignored.
        :param arrow_style: Describes how the fancy arrow will be drawn.
                            It can be string of the available arrowstyle names,
                            with optional comma-separated attributes,
                            or an ArrowStyle instance.
                            The optional attributes are meant to be scaled with
                            the mutation_scale.
        :param connection_style: Describes how the arrow ends are connected.
        :param tail_patch: Optional tail patch.
        :param head_patch: Optional head patch.
        :param tail_shrink_factor: Shrinking factor of the tail.
        :param head_shrink_factor: Shrinking factor of the head.
        :param mutation_scale: Value with which attributes of arrowstyle
                               (e.g., head_length) will be scaled.
        :param mutation_aspect: The height of the rectangle will be squeezed by
                                this value before the mutation and the mutated
                                box will be stretched by the inverse of it.
        :param dpi_cor: dpi_cor is currently used for linewidth-related things
                        and shrink factor. Mutation scale is affected by this.
        :param alpha: Opacity.
        :param cap_style: Cap style.
        :param color: Use to set both the edge-color and the face-color.
        :param edge_color: Edge color.
        :param face_color: Face color.
        :param fill: Whether to fill the rectangle.
        :param join_style: Join style.
        :param label: Label for the object in the legend.
        :param line_style: Line style for edge.
        :param line_width: Line width for edge.
        """
        if line_style and isinstance(line_style, LINE_STYLE):
            line_style = line_style.name
        if cap_style and isinstance(cap_style, CAP_STYLE):
            cap_style = cap_style.name
        if join_style and isinstance(join_style, JOIN_STYLE):
            join_style = join_style.name
        if arrow_style and isinstance(arrow_style, ARROW_STYLE):
            arrow_style = arrow_style.get_name()
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [alpha, cap_style, color, edge_color, face_color,
             fill, join_style, label, line_style, line_width],
            ['alpha', 'capstyle', 'color', 'edgecolor', 'facecolor',
             'fill', 'joinstyle', 'label', 'linestyle', 'linewidth']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        arrow = FancyArrowPatch(
            posA=(x, y), posB=(x + dx, y + dy),
            path=path, arrowstyle=arrow_style,
            connectionstyle=connection_style,
            patchA=tail_patch, patchB=head_patch,
            shrinkA=tail_shrink_factor, shrinkB=head_shrink_factor,
            mutation_scale=mutation_scale, mutation_aspect=mutation_aspect,
            dpi_cor=dpi_cor,
            **kwargs
        )
        self._axes.add_artist(arrow)
        return self

    def add_fancy_box_patch(
            self, x: float, y: float,
            width: float, height: float,
            box_style: Union[str, BoxStyle] = 'Round',
            mutation_scale: Optional[float] = 1,
            mutation_aspect: Optional[float] = None,
            alpha: Optional[float] = None,
            cap_style: Optional[Union[str, CAP_STYLE]] = None,
            color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            face_color: Optional[Color] = None,
            fill: bool = True,
            join_style: Optional[Union[str, JOIN_STYLE]] = None,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[float] = None
    ):
        """
        A fancy box around a rectangle with lower left at xy = (x, y)
        with specified width and height.

        :param x: The left coord of the rectangle.
        :param y: The bottom coord of the rectangle.
        :param width: The rectangle width.
        :param height: The rectangle height.
        :param box_style: The box style.
        :param mutation_scale: Value with which attributes of arrowstyle
                               (e.g., head_length) will be scaled.
        :param mutation_aspect: The height of the rectangle will be squeezed by
                                this value before the mutation and the mutated
                                box will be stretched by the inverse of it.
        :param alpha: Opacity.
        :param cap_style: Cap style.
        :param color: Use to set both the edge-color and the face-color.
        :param edge_color: Edge color.
        :param face_color: Face color.
        :param fill: Whether to fill the rectangle.
        :param join_style: Join style.
        :param label: Label for the object in the legend.
        :param line_style: Line style for edge.
        :param line_width: Line width for edge.
        """
        if line_style and isinstance(line_style, LINE_STYLE):
            line_style = line_style.name
        if cap_style and isinstance(cap_style, CAP_STYLE):
            cap_style = cap_style.name
        if join_style and isinstance(join_style, JOIN_STYLE):
            join_style = join_style.name
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [alpha, cap_style, color, edge_color, face_color,
             fill, join_style, label, line_style, line_width],
            ['alpha', 'capstyle', 'color', 'edgecolor', 'facecolor',
             'fill', 'joinstyle', 'label', 'linestyle', 'linewidth']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        fancy_box = FancyBboxPatch(
            xy=(x, y), width=width, height=height,
            boxstyle=box_style,
            mutation_scale=mutation_scale,
            mutation_aspect=mutation_aspect,
            **kwargs
        )
        self._axes.add_artist(fancy_box)
        return self

    def add_polygon(
            self, xy: ndarray, closed: bool = True,
            alpha: Optional[float] = None,
            color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            face_color: Optional[Color] = None,
            fill: bool = True,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[float] = None,
            cap_style: Optional[Union[str, CAP_STYLE]] = None,
            join_style: Optional[Union[str, JOIN_STYLE]] = None
    ) -> 'AxesFormatter':
        """
        Add a general polygon patch.

        :param xy: A numpy array with shape Nx2.
        :param closed: If True, the polygon will be closed so the starting and
                       ending points are the same.
        :param alpha: Opacity.
        :param cap_style: Cap style.
        :param color: Use to set both the edge-color and the face-color.
        :param edge_color: Edge color.
        :param face_color: Face color.
        :param fill: Whether to fill the rectangle.
        :param join_style: Join style.
        :param label: Label for the object in the legend.
        :param line_style: Line style for edge.
        :param line_width: Line width for edge.
        """
        if line_style and isinstance(line_style, LINE_STYLE):
            line_style = line_style.name
        if cap_style and isinstance(cap_style, CAP_STYLE):
            cap_style = cap_style.name
        if join_style and isinstance(join_style, JOIN_STYLE):
            join_style = join_style.name
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [alpha, cap_style, color, edge_color, face_color,
             fill, join_style, label, line_style, line_width],
            ['alpha', 'capstyle', 'color', 'edgecolor', 'facecolor',
             'fill', 'joinstyle', 'label', 'linestyle', 'linewidth']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        polygon = Polygon(
            xy=xy, closed=closed,
            **kwargs
        )
        self._axes.add_artist(polygon)
        return self

    def add_rectangle(
            self, x: float, y: float, width: float, height: float,
            angle: float = 0.0,
            alpha: Optional[float] = None,
            cap_style: Optional[Union[str, CAP_STYLE]] = None,
            color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            face_color: Optional[Color] = None,
            fill: bool = True,
            join_style: Optional[Union[str, JOIN_STYLE]] = None,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[float] = None
    ) -> 'AxesFormatter':
        """
        Add a rectangle to the Axes.

        :param x: The left rectangle coordinate.
        :param y: The bottom rectangle coordinate.
        :param width: Rectangle width.
        :param height: Rectangle height.
        :param angle: Rotation in degrees anti-clockwise about xy
                      (default is 0.0)
        :param alpha: Opacity.
        :param cap_style: Cap style.
        :param color: Use to set both the edge-color and the face-color.
        :param edge_color: Edge color.
        :param face_color: Face color.
        :param fill: Whether to fill the rectangle.
        :param join_style: Join style.
        :param label: Label for the object in the legend.
        :param line_style: Line style for edge.
        :param line_width: Line width for edge.
        """
        if line_style and isinstance(line_style, LINE_STYLE):
            line_style = line_style.name
        if cap_style and isinstance(cap_style, CAP_STYLE):
            cap_style = cap_style.name
        if join_style and isinstance(join_style, JOIN_STYLE):
            join_style = join_style.name
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [alpha, cap_style, color, edge_color, face_color,
             fill, join_style, label, line_style, line_width],
            ['alpha', 'capstyle', 'color', 'edgecolor', 'facecolor',
             'fill', 'joinstyle', 'label', 'linestyle', 'linewidth']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        rectangle = Rectangle(
            xy=(x, y), width=width, height=height, angle=angle,
            **kwargs
        )
        self._axes.add_artist(rectangle)
        return self

    def add_regular_polygon(
            self, x: float, y: float,
            num_vertices: int,
            radius: float,
            angle: float = 0,
            alpha: Optional[float] = None,
            color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            face_color: Optional[Color] = None,
            fill: bool = True,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[float] = None,
            cap_style: Optional[Union[str, CAP_STYLE]] = None,
            join_style: Optional[Union[str, JOIN_STYLE]] = None
    ) -> 'AxesFormatter':
        """
        Add a rectangle to the Axes.

        :param x: The left rectangle coordinate.
        :param y: The bottom rectangle coordinate.
        :param num_vertices: Number of vertices.
        :param radius: The distance from the center to each of the vertices.
        :param angle: Rotation in degrees anti-clockwise about xy
                            (default is 0.0)
        :param alpha: Opacity.
        :param cap_style: Cap style.
        :param color: Use to set both the edge-color and the face-color.
        :param edge_color: Edge color.
        :param face_color: Face color.
        :param fill: Whether to fill the rectangle.
        :param join_style: Join style.
        :param label: Label for the object in the legend.
        :param line_style: Line style for edge.
        :param line_width: Line width for edge.
        """
        if line_style and isinstance(line_style, LINE_STYLE):
            line_style = line_style.name
        if cap_style and isinstance(cap_style, CAP_STYLE):
            cap_style = cap_style.name
        if join_style and isinstance(join_style, JOIN_STYLE):
            join_style = join_style.name
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [alpha, cap_style, color, edge_color, face_color,
             fill, join_style, label, line_style, line_width],
            ['alpha', 'capstyle', 'color', 'edgecolor', 'facecolor',
             'fill', 'joinstyle', 'label', 'linestyle', 'linewidth']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        polygon = RegularPolygon(
            xy=(x, y), numVertices=num_vertices, radius=radius,
            orientation=pi * angle / 180,
            **kwargs
        )
        self._axes.add_artist(polygon)
        return self

    def add_wedge(
            self, x: float, y: float, radius: float,
            theta_start: float, theta_end: float,
            width: Optional[float] = None,
            alpha: Optional[float] = None,
            cap_style: Optional[Union[str, CAP_STYLE]] = None,
            color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            face_color: Optional[Color] = None,
            fill: bool = True,
            join_style: Optional[Union[str, JOIN_STYLE]] = None,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[float] = None
    ):
        """
        Add a wedge-shaped patch.

        :param x: The x-coordinate of the center of the ellipse.
        :param y: The y-coordinate of the center of the ellipse.
        :param radius: (Outer) radius.
        :param theta_start: Starting angle of the arc in degrees.
                            Relative to angle, e.g. if angle = 45 and
                            theta_start = 90 the absolute starting angle is 135.
        :param theta_end: Ending angle of the arc in degrees.
        :param width: If width is given, then a partial wedge is drawn from
                      inner radius r - width to outer radius r.
        :param alpha: Opacity.
        :param cap_style: Cap style.
        :param color: Use to set both the edge-color and the face-color.
        :param edge_color: Edge color.
        :param face_color: Face color.
        :param fill: Whether to fill the rectangle.
        :param join_style: Join style.
        :param label: Label for the object in the legend.
        :param line_style: Line style for edge.
        :param line_width: Line width for edge.
        """
        if line_style and isinstance(line_style, LINE_STYLE):
            line_style = line_style.name
        if cap_style and isinstance(cap_style, CAP_STYLE):
            cap_style = cap_style.name
        if join_style and isinstance(join_style, JOIN_STYLE):
            join_style = join_style.name
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [alpha, cap_style, color, edge_color, face_color,
             fill, join_style, label, line_style, line_width],
            ['alpha', 'capstyle', 'color', 'edgecolor', 'facecolor',
             'fill', 'joinstyle', 'label', 'linestyle', 'linewidth']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        arc = Wedge(
            center=(x, y), r=radius,
            theta1=theta_start, theta2=theta_end,
            width=width,
            **kwargs
        )
        self._axes.add_artist(arc)
        return self

    @property
    def arcs(self) -> PatchListFormatter:
        """
        Return a list of the Arcs on the axes.
        """
        return PatchListFormatter([
            a for a in self._axes.get_children()
            if isinstance(a, Arc)
        ])

    @property
    def arrows(self) -> PatchListFormatter:
        """
        Return a list of the Arrows on the axes.
        """
        return PatchListFormatter([
            a for a in self._axes.get_children()
            if isinstance(a, Arrow)
        ])

    @property
    def circles(self) -> PatchListFormatter:
        """
        Return a list of the Circles on the axes.
        """
        return PatchListFormatter([
            c for c in self._axes.get_children()
            if isinstance(c, Circle)
        ])

    @property
    def ellipses(self) -> PatchListFormatter:
        """
        Return a list of the Ellipses on the axes.
        """
        return PatchListFormatter([
            e for e in self._axes.get_children()
            if isinstance(e, Ellipse)
        ])

    @property
    def fancy_arrows(self) -> PatchListFormatter:
        """
        Return a list of the FancyArrows on the axes.
        """
        return PatchListFormatter([
            a for a in self._axes.get_children()
            if isinstance(a, FancyArrow)
        ])

    @property
    def fancy_arrow_patches(self) -> PatchListFormatter:
        """
        Return a list of the FancyArrowPatches on the axes.
        """
        return PatchListFormatter([
            a for a in self._axes.get_children()
            if isinstance(a, FancyArrowPatch)
        ])

    @property
    def fancy_boxes(self) -> PatchListFormatter:
        """
        Return a list of the FancyBoxes on the axes.
        """
        return PatchListFormatter([
            b for b in self._axes.get_children()
            if isinstance(b, FancyBboxPatch)
        ])

    @property
    def polygons(self) -> PatchListFormatter:
        """
        Return a list of the Polygons on the axes.
        """
        return PatchListFormatter([
            p for p in self._axes.get_children()
            if isinstance(p, Polygon)
        ])

    @property
    def rectangles(self) -> PatchListFormatter:
        """
        Return a list of the Rectangles on the axes.
        """
        return PatchListFormatter([
            r for r in self._axes.get_children()
            if isinstance(r, Rectangle)
        ])

    @property
    def regular_polygons(self) -> PatchListFormatter:
        """
        Return a list of the RegularPolygons on the axes.
        """
        return PatchListFormatter([
            r for r in self._axes.get_children()
            if isinstance(r, RegularPolygon)
        ])

    @property
    def wedges(self) -> PatchListFormatter:
        """
        Return a list of the Wedges on the axes.
        """
        return PatchListFormatter([
            w for w in self._axes.get_children()
            if isinstance(w, Wedge)
        ])

    # endregion

    # region custom shapes

    def add_v_density(
            self, x: float,
            y_to_z: Series,
            color: Color,
            color_min: Optional[Color] = None,
            width: float = 0.8,
            z_max: Optional[float] = None,
            h_align: str = 'center'
    ) -> 'AxesFormatter':
        """
        Add a vertical density bar to the plot.

        :param x: The x-coordinate of the bar.
        :param y_to_z: A mapping of the bar's y-coordinate to it density.
        :param color: The color of the density bar.
        :param color_min: Optional 2nd color to fade out to.
        :param width: The bar width.
        :param z_max: Value to scale down densities by to get to a range of
                      0 to 1. Defaults to max value of y_to_z.
        :param h_align: Horizontal alignment. One of {'left', 'center', 'right'}
        """
        check_h_align(h_align)

        if z_max is None:
            z_max = y_to_z.max()
        y = y_to_z.index.to_list()
        y_lowers = y[: -1]
        y_uppers = y[1:]

        if h_align == 'left':
            x_p = x
        elif h_align == 'center':
            x_p = x - width / 2
        else:
            x_p = x - width

        alphas = (y_to_z / z_max).rolling(2).mean().shift(-1).dropna()

        if color_min is None:
            color_min = color
        colors = cross_fade(from_color=color_min, to_color=color, amount=alphas)

        for y_lower, y_upper, alpha, color in zip(
                y_lowers, y_uppers, alphas, colors
        ):
            self.add_rectangle(
                x=x_p, y=y_lower,
                width=width, height=y_upper - y_lower,
                face_color=color, alpha=alpha
            )

        return self

    # endregion

    # region plots

    def add_v_bars(
            self,
            x: Union[str, FloatOrFloatIterable],
            y: Union[str, FloatOrFloatIterable],
            width: Union[str, FloatOrFloatIterable],
            box_style: Union[BoxStyle, Iterable[BoxStyle]],
            data: Optional[DataFrame] = None,
            y_0: Optional[Union[str, FloatOrFloatIterable]] = 0.0,
            h_align: str = 'center',
            mutation_scale: Union[str, FloatOrFloatIterable] = 1,
            mutation_aspect: Optional[Union[str, FloatOrFloatIterable]] = None,
            alpha: Optional[Union[str, FloatOrFloatIterable]] = None,
            cap_style: Optional[Union[
                StrOrStrIterable, CAP_STYLE, Iterable[CAP_STYLE]
            ]] = None,
            color: Optional[ColorOrColorIterable] = None,
            edge_color: Optional[ColorOrColorIterable] = None,
            face_color: Optional[ColorOrColorIterable] = None,
            fill: BoolOrBoolIterable = True,
            line_style: Optional[Union[
                StrOrStrIterable, LINE_STYLE, Iterable[LINE_STYLE]
            ]] = None,
            line_width: Optional[FloatOrFloatIterable] = None
    ) -> 'AxesFormatter':
        """
        Add vertical bars to the plot with the given BoxStyle.

        :param x: X-coordinate for each bar, or name of column.
        :param y: Y-coordinate of top of each bar, or name of column.
        :param width: Width of each bar, or name of column.
        :param box_style: The style of each box, or name of column.
        :param data: Optional DataFrame to extract sequences of attributes.
        :param y_0: Y-coordinate of bottom of each bar. Defaults to 0.
        :param h_align: Horizontal alignment. One of {'left', 'center', 'right'}
        :param mutation_scale: Scaling factor applied to the attributes of the
                               box style (e.g. pad or rounding_size).
        :param mutation_aspect: The height of the rectangle will be squeezed by
                                this value before the mutation and the mutated
                                box will be stretched by the inverse of it.
                                For example, this allows different horizontal
                                and vertical padding.
        :param alpha: Opacity from 0 to 1.
        :param cap_style: One of {'butt', 'round', 'projecting'}
        :param color: Color for faces and edges.
        :param edge_color: Color for edges.
        :param face_color: Color for faces.
        :param fill: Whether bars are filled.
        :param line_style: Line style.
        :param line_width: Line width.
        """
        check_h_align(h_align)

        def get_data(item) -> Series:
            if data is None:
                return item
            if isinstance(item, str) and item in data.columns:
                return data[item]
            else:
                return item

        def make_iterable(item):
            if not isinstance(item, Iterable) or isinstance(item, str):
                item = [item] * len(x)
            return item

        x = get_data(x)
        y = make_iterable(get_data(y))
        y_0 = make_iterable(get_data(y_0))
        width = make_iterable(get_data(width))
        box_style = make_iterable(get_data(box_style))
        mutation_scale = make_iterable(get_data(mutation_scale))
        mutation_aspect = make_iterable(get_data(mutation_aspect))
        alpha = make_iterable(get_data(alpha))
        cap_style = make_iterable(get_data(cap_style))
        color = make_iterable(get_data(color))
        edge_color = make_iterable(get_data(edge_color))
        face_color = make_iterable(get_data(face_color))
        fill = make_iterable(get_data(fill))
        line_style = make_iterable(get_data(line_style))
        line_width = make_iterable(get_data(line_width))

        for (
                x_i, y_i, y_0_i, w_i, bs_i,
                ms_i, ma_i, a_i, cs_i,
                c_i, ec_i, fc_i,
                f_i, ls_i, lw_i
        ) in zip(
            x, y, y_0, width, box_style,
            mutation_scale, mutation_aspect, alpha, cap_style,
            color, edge_color, face_color,
            fill, line_style, line_width
        ):
            if h_align == 'left':
                x_p = x_i
            elif h_align == 'center':
                x_p = x_i - w_i / 2
            else:
                x_p = x_i - width

            self.add_fancy_box_patch(
                x=x_p, y=y_0_i, width=w_i, height=y_i - y_0_i,
                box_style=bs_i,
                mutation_scale=ms_i, mutation_aspect=ma_i,
                alpha=a_i, cap_style=cs_i,
                color=c_i, edge_color=ec_i, face_color=fc_i,
                fill=f_i, line_style=ls_i, line_width=lw_i
            )

        return self

    def add_v_pills(
            self,
            x: Union[str, FloatOrFloatIterable],
            y: Union[str, FloatOrFloatIterable],
            width: float,
            data: Optional[DataFrame] = None,
            y_0: Optional[Union[str, FloatOrFloatIterable]] = 0.0,
            h_align: str = 'center',
            alpha: Optional[Union[str, FloatOrFloatIterable]] = None,
            color: Optional[ColorOrColorIterable] = None,
            edge_color: Optional[ColorOrColorIterable] = None,
            face_color: Optional[ColorOrColorIterable] = None,
            fill: BoolOrBoolIterable = True,
            line_style: Optional[Union[
                StrOrStrIterable, LINE_STYLE, Iterable[LINE_STYLE]
            ]] = None,
            line_width: Optional[FloatOrFloatIterable] = None
    ) -> 'AxesFormatter':
        """
        Add vertical bars to the plot with the given BoxStyle.

        :param x: X-coordinate for each bar, or name of column.
        :param y: Y-coordinate of top of each bar, or name of column.
        :param width: Width of each bar, or name of column.
        :param data: Optional DataFrame to extract sequences of attributes.
        :param y_0: Y-coordinate of bottom of each bar. Defaults to 0.
        :param h_align: One of {'left', 'center', 'right'}.
        :param alpha: Opacity from 0 to 1.
        :param color: Color for faces and edges.
        :param edge_color: Color for edges.
        :param face_color: Color for faces.
        :param fill: Whether bars are filled.
        :param line_style: Line style.
        :param line_width: Line width.
        """
        mutation_aspect = (
                (self.width() / self.height()) *
                (self.get_y_height() / self.get_x_width())
        )
        self.add_v_bars(
            data=data, x=x, y=y, width=width,
            box_style=BoxStyle.Round(pad=0.0, rounding_size=width / 2),
            y_0=y_0, h_align=h_align,
            mutation_aspect=mutation_aspect,
            alpha=alpha,
            color=color, edge_color=edge_color, face_color=face_color,
            fill=fill, line_style=line_style, line_width=line_width
        )
        return self

    def add_line(
            self,
            x: FloatIterable, y: FloatIterable,
            smooth: Union[bool, int] = False, smooth_order: int = 2,
            alpha: Optional[float] = None,
            color: Optional[Color] = None,
            draw_style: Optional[Union[str, DRAW_STYLE]] = None,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[float] = None,
            marker: Optional[Union[str, MARKER_STYLE]] = None,
            marker_edge_color: Optional[Color] = None,
            marker_edge_width: Optional[float] = None,
            marker_face_color: Optional[Color] = None,
            marker_face_color_alt: Optional[Color] = None,
            marker_size: Optional[float] = None,
    ) -> 'AxesFormatter':
        """
        Add a line to the plot.

        :param x: X-coordinates of the line.
        :param y: Y-coordinates of the line.
        :param smooth: True or False or number of points. True -> 1,000 points.
        :param smooth_order: Order for smoothing e.g. 2 = quadratic, 3 = cubic
        :param alpha: Opacity of the line.
        :param color: Color of the line.
        :param draw_style: Draw style. One of {'default', 'steps', 'steps-pre',
                           'steps-mid', 'steps-post'}
        :param label: Label.
        :param line_style: Line Style. One of {'-', '--', '-.', ':', '',
                           (offset, on-off-seq), ...}
        :param line_width: Line width.
        :param marker: Marker style.
        :param marker_edge_color: Marker edge color.
        :param marker_edge_width: Marker edge width.
        :param marker_face_color: Marker face color.
        :param marker_face_color_alt: Alt marker face color.
        :param marker_size: Marker size.
        """
        if smooth is not False:
            if smooth is True:
                smooth = 1000
            f_smooth = interp1d(x, y, kind=smooth_order)
            x_smooth = linspace(min(x), max(x), smooth)
            y_smooth = f_smooth(x_smooth)
            x = x_smooth
            y = y_smooth

        draw_style = (
            draw_style if isinstance(draw_style, str)
            else DRAW_STYLE.get_name(draw_style)
        )
        line_style = (
            line_style if isinstance(line_style, str)
            else LINE_STYLE.get_name(line_style)
        )

        self._axes.plot(
            x, y, alpha=alpha, color=color,
            drawstyle=draw_style,
            label=label,
            ls=line_style,
            lw=line_width,
            marker=marker,
            markersize=marker_size,
            mec=marker_edge_color,
            mew=marker_edge_width,
            mfc=marker_face_color,
            mfcalt=marker_face_color_alt
        )
        return self

    # endregion

    # endregion

    def set_title_font_family(self, font_name: str) -> 'AxesFormatter':
        """
        Set the font family for the Axes title.

        :param font_name: Name of the font.
        """
        self.title.set_font_family(font_name)
        return self

    # region limits

    def get_x_lim(self) -> Tuple[float, float]:
        """
        Return the x-axis view limits.
        """
        return self._axes.get_xlim()

    def get_y_lim(self) -> Tuple[float, float]:
        """
        Return the y-axis view limits.
        """
        return self._axes.get_ylim()

    def set_x_lim(self, left: Optional[float] = None,
                  right: Optional[float] = None) -> 'AxesFormatter':
        """
        Set the limits of the x-axis.

        :param left: Lower limit.
        :param right: Upper limit.
        """
        self._axes.set_xlim(left=left, right=right)
        return self

    def set_y_lim(self, bottom: Optional[float] = None,
                  top: Optional[float] = None) -> 'AxesFormatter':
        """
        Set the limits of the y-axis.

        :param bottom: Lower limit.
        :param top: Upper limit.
        """
        self._axes.set_ylim(bottom=bottom, top=top)
        return self

    def get_x_min(self) -> float:
        """
        Return the x-axis lower view limit.
        """
        return self.get_x_lim()[0]

    def get_x_max(self) -> float:
        """
        Return the x-axis upper view limit.
        """
        return self.get_x_lim()[1]

    def get_x_width(self) -> float:

        return abs(self.get_x_max() - self.get_x_min())

    def get_y_height(self) -> float:

        return abs(self.get_y_max() - self.get_y_min())

    def set_x_min(self, left: float = None) -> 'AxesFormatter':
        """
        Set the x-axis lower view limit.
        """
        self.set_x_lim(left, None)
        return self

    def set_x_max(self, right: float = None) -> 'AxesFormatter':
        """
        Set the x-axis upper view limit.
        """
        self.set_x_lim(None, right)
        return self

    def get_y_min(self) -> float:
        """
        Return the y-axis lower view limit.
        """
        return self.get_y_lim()[0]

    def get_y_max(self) -> float:
        """
        Return the y-axis upper view limit.
        """
        return self.get_y_lim()[1]

    def set_y_min(self, left: float = None) -> 'AxesFormatter':
        """
        Set the y-axis lower view limit.
        """
        self.set_y_lim(left, None)
        return self

    def set_y_max(self, right: float = None) -> 'AxesFormatter':
        """
        Set the y-axis upper view limit.
        """
        self.set_y_lim(None, right)
        return self

    def width(self, units: str = 'inches') -> float:

        if units not in ('inches', 'pixels'):
            raise ValueError("units not in ('inches', 'pixels')")
        fig = self._axes.figure
        bbox = self.axes.get_window_extent().transformed(
            fig.dpi_scale_trans.inverted()
        )
        width = bbox.width
        if units == 'pixels':
            width *= fig.dpi
        return width

    def height(self, units: str = 'inches') -> float:

        if units not in ('inches', 'pixels'):
            raise ValueError("units not in ('inches', 'pixels')")
        fig = self._axes.figure
        bbox = self.axes.get_window_extent().transformed(
            fig.dpi_scale_trans.inverted()
        )
        height = bbox.height
        if units == 'pixels':
            height *= fig.dpi
        return height

    # endregion

    def grid(self, value: bool = True,
             which: str = 'major',
             axis: str = 'both') -> 'AxesFormatter':
        """
        Turn the grid on or off.

        :param value: True or False. Defaults to True.
        :param which: 'major', 'minor' or 'both'
        :param axis: 'x', 'y' or 'both
        """
        self._axes.grid(b=value, which=which, axis=axis)
        return self

    def set_axis_below(self,
                       value: bool = True) -> 'AxesFormatter':
        """
        Set whether axis ticks and gridlines are above or below most artists.

        :param value: True or False
        """
        self._axes.set_axisbelow(b=value)
        return self

    def save(self,
             file_path: Union[str, Path],
             file_type: Optional[str] = None) -> 'AxesFormatter':
        """
        Save the plot to disk.

        :param file_path: The file path to save the plot object to.
        :param file_type: The type of file to save.
                          Defaults to png if can't be auto-detected from name.
        """
        save_plot(plot_object=self._axes,
                  file_path=file_path,
                  file_type=file_type)
        return self

    def tight_layout(self) -> 'AxesFormatter':
        """
        Call the tight_layout method on the Axes' figure.
        """
        self._axes.figure.tight_layout()
        return self

    def invert_x_axis(self) -> 'AxesFormatter':
        """
        Invert the x-axis.
        """
        self.x_axis.invert()
        return self

    def invert_y_axis(self) -> 'AxesFormatter':
        """
        Invert the y-axis.
        """
        self.y_axis.invert()
        return self

    def add_legend(
            self,
            handles: Optional[List[PathCollection]] = None,
            labels: Optional[List[str]] = None,
            location: Optional[LegendLocation] = None,
            n_cols: Optional[int] = None,
            font_size: Optional[str] = None,
            font_properties: Optional[Union[FontProperties, dict]] = None,
            line_points: Optional[int] = None,
            scatter_points: Optional[int] = None,
            scatter_y_offsets: Optional[ArrayLike] = None,
            marker_scale: Optional[float] = None,
            frame_on: Optional[bool] = None,
            shadow: Optional[bool] = None,
            frame_alpha: Optional[float] = None,
            face_color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            mode: Optional[str] = None,
            title: Optional[str] = None,
            title_font_size: Optional[FontSize] = None,
            label_spacing: Optional[float] = None,
            handle_length: Optional[float] = None,
            handle_text_pad: Optional[float] = None,
            border_axes_pad: Optional[float] = None,
            column_spacing: Optional[float] = None
    ) -> LegendFormatter:
        """
        Add a legend to the Axes.

        :param handles: A list of Artists (lines, patches) to be added to the
                        legend.
        :param labels: A list of labels to show next to the artists. The length
                       of handles and labels should be the same. If they are
                       not, they are truncated to the smaller of both lengths.
        :param location: The legend location.
        :param n_cols: The number of columns that the legend has. Default is 1.
        :param font_size: The font size of the legend. If the value is numeric
                          the size will be the absolute font size in points.
                          String values are relative to the current default font
                          size. This argument is only used if font_properties is
                          not specified.
        :param font_properties: The font properties of the legend. If None
                                (default), the current matplotlib.rcParams will
                                be used.
        :param line_points: The number of marker points in the legend when
                            creating a legend entry for a Line2D (line).
                            Default is None, which means using
                            rcParams["legend.numpoints"] (default: 1).
        :param scatter_points: The number of marker points in the legend when
                               creating a legend entry for a PathCollection
                               (scatter plot). Default is None, which means using
                               rcParams["legend.scatterpoints"] (default: 1).
        :param scatter_y_offsets: The vertical offset (relative to the font size)
                                  for the markers created for a scatter plot
                                  legend entry. 0.0 is at the base the legend
                                  text, and 1.0 is at the top. To draw all
                                  markers at the same height, set to [0.5].
                                  Default is [0.375, 0.5, 0.3125].
        :param marker_scale: The relative size of legend markers compared with
                             the originally drawn ones. Default is None, which
                             means using rcParams["legend.markerscale"]
                             (default: 1.0).
        :param frame_on: Whether the legend should be drawn on a patch (frame).
                         Default is None, which means using
                         rcParams["legend.frameon"] (default: True).
        :param shadow: Whether to draw a shadow behind the legend. Default is
                       None, which means using rcParams["legend.shadow"]
                       (default: False).
        :param frame_alpha: The alpha transparency of the legend's background.
                            Default is None, which means using
                            rcParams["legend.framealpha"] (default: 0.8). If
                            shadow is activated and framealpha is None, the
                            default value is ignored.
        :param face_color: The legend's background color. Default is None, which
                           means using rcParams["legend.facecolor"]
                           (default: 'inherit'). If "inherit", use
                           rcParams["axes.facecolor"] (default: 'white').
        :param edge_color: The legend's background patch edge color. Default is
                           None, which means using rcParams["legend.edgecolor"]
                           (default: '0.8'). If "inherit", use take
                           rcParams["axes.edgecolor"] (default: 'black').
        :param mode: If mode is set to "expand" the legend will be horizontally
                     expanded to fill the axes area (or bbox_to_anchor if
                     defines the legend's size).
        :param title: The legend's title. Default is no title (None).
        :param title_font_size: The fontsize of the legend's title. Default is
                                the default fontsize.
        :param label_spacing: The fractional whitespace inside the legend border,
                              in font-size units. Default is None, which means
                              using rcParams["legend.borderpad"] (default: 0.4).
        :param handle_length: The length of the legend handles, in font-size
                              units. Default is None, which means using
                              rcParams["legend.handlelength"] (default: 2.0).
        :param handle_text_pad: The pad between the legend handle and text, in
                                font-size units. Default is None, which means
                                using rcParams["legend.handletextpad"]
                                (default: 0.8).
        :param border_axes_pad: The pad between the axes and legend border, in
                                font-size units. Default is None,
                                which means using
                                rcParams["legend.borderaxespad"] (default: 0.5).
        :param column_spacing: The spacing between columns, in font-size units.
                               Default is None, which means using
                               rcParams["legend.columnspacing"] (default: 2.0).
        """
        kwargs = {}
        for kwarg, mpl_arg in zip(
            [handles, labels, n_cols, font_properties, font_size,
             line_points, scatter_points, scatter_y_offsets, marker_scale,
             frame_on, shadow, frame_alpha, face_color, edge_color,
             mode, title, title_font_size, label_spacing, handle_length,
             handle_text_pad, border_axes_pad, column_spacing, location],
            ['handles', 'labels', 'ncol', 'prop', 'fontsize',
             'numpoints', 'scatterpoints', 'scatteryoffsets', 'markerscale',
             'frameon', 'shadow', 'framealpha', 'facecolor', 'edgecolor',
             'mode', 'title', 'title_fontsize', 'labelspacing', 'handlelength',
             'handletextpad', 'borderaxespad', 'columnspacing', 'loc']
        ):
            if kwarg is not None:
                kwargs[mpl_arg] = kwarg
        self._legend = LegendFormatter(self._axes.legend(**kwargs))
        return self._legend

    def show(self) -> 'AxesFormatter':
        """
        Show the figure for the axes.
        """
        plt.show()
        return self
