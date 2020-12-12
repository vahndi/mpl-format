from mpl_format.animation.kwarg_animations.color_animation import ColorAnimation
from mpl_format.animation.kwarg_animations.float_animation import FloatAnimation
from mpl_format.axes import AxesFormatter


class ShapeAnimation(object):

    def draw(self, t: float, axes: AxesFormatter) -> dict:

        raise NotImplementedError

    def add_non_animated_kwarg(self, arg_name: str, kwargs: dict):

        value = getattr(self, arg_name)
        if value is not None:
            kwargs[arg_name] = value

    def add_color_kwarg(self, arg_name: str, kwargs: dict, t: float):

        value = getattr(self, arg_name)
        if value is not None:
            kwargs[arg_name] = (
                value.at(t) if isinstance(value, ColorAnimation)
                else value
            )

    def add_float_kwarg(self, arg_name: str, kwargs: dict, t: float):

        value = getattr(self, arg_name)
        if value is not None:
            kwargs[arg_name] = (
                value.at(t) if isinstance(value, FloatAnimation)
                else value
            )

