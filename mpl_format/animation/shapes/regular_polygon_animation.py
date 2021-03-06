from typing import Optional, Union

from mpl_format.animation.shapes.base import ShapeAnimation
from mpl_format.animation.type_animations import FloatOrFloatAnimation, \
    StrOrFloatOrFloatAnimation, ColorOrColorAnimation
from mpl_format.axes import AxesFormatter
from mpl_format.enums.join_style import JOIN_STYLE
from mpl_format.enums.cap_style import CAP_STYLE
from mpl_format.enums.line_style import LINE_STYLE


class RegularPolygonAnimation(ShapeAnimation, object):

    def __init__(
            self,
            x_center: FloatOrFloatAnimation,
            y_center: FloatOrFloatAnimation,
            num_vertices: int,
            radius: FloatOrFloatAnimation,
            angle: FloatOrFloatAnimation = 0,
            alpha: Optional[StrOrFloatOrFloatAnimation] = None,
            color: Optional[ColorOrColorAnimation] = None,
            edge_color: Optional[ColorOrColorAnimation] = None,
            face_color: Optional[ColorOrColorAnimation] = None,
            fill: bool = True,
            label: Optional[str] = None,
            line_style: Optional[Union[str, LINE_STYLE]] = None,
            line_width: Optional[FloatOrFloatAnimation] = None,
            cap_style: Optional[Union[str, CAP_STYLE]] = None,
            join_style: Optional[Union[str, JOIN_STYLE]] = None,
    ):
        self.x_center: FloatOrFloatAnimation = x_center
        self.y_center: FloatOrFloatAnimation = y_center
        self.num_vertices: int = num_vertices
        self.radius: FloatOrFloatAnimation = radius
        self.angle: FloatOrFloatAnimation = angle
        self.alpha: Optional[FloatOrFloatAnimation] = self._float_anim(alpha)
        self.color: Optional[ColorOrColorAnimation] = color
        self.edge_color: Optional[ColorOrColorAnimation] = edge_color
        self.face_color: Optional[ColorOrColorAnimation] = face_color
        self.fill: bool = fill
        self.label: Optional[str] = label
        self.line_style: Optional[Union[str, LINE_STYLE]] = line_style
        self.line_width: Optional[FloatOrFloatAnimation] = line_width
        self.cap_style: Optional[Union[str, CAP_STYLE]] = cap_style
        self.join_style: Optional[Union[str, JOIN_STYLE]] = join_style

    def draw(self, t: float, axes: AxesFormatter):

        kwargs = {}
        for float_kwarg in ('x_center', 'y_center', 'radius',
                            'angle', 'alpha', 'line_width'):
            self._add_float_kwarg(float_kwarg, kwargs, t)
        for color_kwarg in ('color', 'edge_color', 'face_color'):
            self._add_color_kwarg(color_kwarg, kwargs, t)
        for kwarg in ('num_vertices', 'fill', 'label',
                      'line_style', 'cap_style', 'join_style'):
            self._add_non_animated_kwarg(kwarg, kwargs)

        axes.add_regular_polygon(**kwargs)
