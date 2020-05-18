from matplotlib.axis import Axis
import matplotlib.pyplot as plt
from matplotlib.text import Text
from matplotlib.ticker import StrMethodFormatter
from typing import Union, Dict, Callable

from mpl_format.text.text_formatter import TextFormatter
from mpl_format.text.text_utils import wrap_text, map_text


class AxisFormatter(object):

    def __init__(self, axis: Axis):
        """
        Create a new AxisFormatter

        :param axis: The matplotlib Axis instance to wrap.
        """
        self._axis: Axis = axis
        self._label: TextFormatter = TextFormatter(self._axis.label)

    @property
    def axis(self) -> Axis:
        """
        Return the wrapped matplotlib Axis object.
        """
        return self._axis

    @property
    def label(self) -> TextFormatter:
        """
        Return a TextFormatter wrapping the axis label.
        """
        return self._label

    def rotate_label(self, rotation: int, how: str = 'absolute') -> 'AxisFormatter':
        """
        Set the rotation of the axis label.

        :param rotation: The rotation value to set in degrees.
        :param how: 'absolute' or 'relative'
        """
        self.label.rotate(rotation, how)
        return self

    def rotate_tick_labels(self, rotation: int, how: str = 'absolute') -> 'AxisFormatter':
        """
        Set the rotation of axis tick labels.

        :param rotation: The rotation value to set in degrees.
        :param how: 'absolute' or 'relative'
        """
        label: Text
        if self._axis.get_majorticklabels():
            for label in self._axis.get_majorticklabels():
                if how == 'relative':
                    label.set_rotation(label.get_rotation() + rotation)
                else:
                    label.set_rotation(label.get_rotation())
            plt.setp(self._axis.get_majorticklabels(), rotation=rotation)
        if self._axis.get_minorticklabels():
            plt.setp(self._axis.get_minorticklabels(), rotation=rotation)
        return self

    def wrap_label(self, max_width: int) -> 'AxisFormatter':
        """
        Wrap the axis label text if it exceeds a given width of characters.
        :param max_width: The maximum character width per line.
        """
        self.label.wrap(max_width=max_width)
        return self

    def wrap_tick_labels(self, max_width: int) -> 'AxisFormatter':
        """
        Wrap the text for each tick label with new lines if it exceeds
        a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self._axis.set_ticklabels([
            wrap_text(text, max_width)
            for text in self._axis.get_ticklabels()
        ])

    def set_format_integer(self, separator: str = ',') -> 'AxisFormatter':
        """
        Format an axis with currency symbols and separators.

        :param separator: The symbol to separate each group of 3 digits.
        """
        fmt = '{x:%s.0f}' % separator
        tick = StrMethodFormatter(fmt)
        self._axis.set_major_formatter(tick)
        return self

    def set_format_currency(self, symbol: str = '$', num_decimals: int = 0) -> 'AxisFormatter':
        """
        Format an axis with currency symbols and separators.

        :param symbol: The currency symbol to use.
        :param num_decimals: The number of decimal places to use (typically 0 or 2).
        """
        fmt = '%s{x:,.%sf}' % (symbol, num_decimals)
        tick = StrMethodFormatter(fmt)
        self._axis.set_major_formatter(tick)
        return self

    def set_label_text(self, text: str) -> 'AxisFormatter':
        """
        Set the text of the Axis label.
        """
        self.label.set_text(text)
        return self

    def set_label_size(self, font_size: int) -> 'AxisFormatter':
        """
        Set the font size for the axis label.
        """
        self.label.set_size(font_size)
        return self

    def set_tick_label_size(self, font_size: int) -> 'AxisFormatter':
        """
        Set the font size for the axis tick labels.
        """
        self._axis.set_tick_params(labelsize=font_size)
        return self

    def map_tick_labels(self, mapping: Union[Dict[str, str], Callable[[str], str]]) -> 'AxisFormatter':
        """
        Map the tick label text using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        labels = [label.get_text() for label in self._axis.get_ticklabels()]
        self._axis.set_ticklabels(map_text(labels, mapping))
        return self

    def set_scale_log(self) -> 'AxisFormatter':
        """
        Set the scale of the axis to logarithmic.
        """
        self._axis._set_scale('log')
        return self

    def set_scale_linear(self) -> 'AxisFormatter':
        """
        Set the scale of the axis to logarithmic.
        """
        self._axis._set_scale('linear')
        return self

    def set_scale_symmetrical_log(self) -> 'AxisFormatter':
        """
        Set the scale of the axis to symmetrical logarithmic.
        """
        self._axis._set_scale('symlog')
        return self

    def set_scale_logit(self) -> 'AxisFormatter':
        """
        Set the scale of the axis to logit.
        """
        self._axis._set_scale('logit')
        return self

    def set_inverted(self, inverted: bool = True) -> 'AxisFormatter':
        """
        Invert the Axis.
        """
        self._axis.set_inverted(inverted=inverted)
        return self

    def invert(self) -> 'AxisFormatter':
        """
        Invert the Axis.
        """
        self._axis.set_inverted(inverted=not self._axis.get_inverted())

    def replace_label_text(self, old: str, new: str) -> 'AxisFormatter':
        """
        Replace the old label text with the new.
        """
        self.label.replace(old=old, new=new)
        return self
