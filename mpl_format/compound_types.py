from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Patch
from matplotlib.path import Path
from numpy import ndarray
from seaborn import JointGrid, PairGrid
from typing import TypeVar, Tuple, Union, Dict, Callable, Iterable, List, Sized

from mpl_format.enums import FONT_SIZE, FONT_STRETCH, FONT_WEIGHT, FONT_STYLE, \
    FONT_VARIANT, CAP_STYLE, JOIN_STYLE, LINE_STYLE, ARROW_STYLE, \
    CONNECTION_STYLE
from mpl_format.enums.box_style import BoxStyleType

# built-ins
BoolIterable = Iterable[bool]
DictIterable = Iterable[dict]
FloatIterable = Iterable[float]
IntIterable = Iterable[int]
StrIterable = Iterable[str]
NdArrayIterable = Iterable[ndarray]
BoolList = List[bool]
DictList = List[dict]
FloatList = List[float]
IntList = List[int]
StrList = List[str]
BoolOrBoolIterable = Union[bool, BoolIterable]
DictOrDictIterable = Union[dict, DictIterable]
FloatOrFloatIterable = Union[float, FloatIterable]
IntOrIntIterable = Union[int, IntIterable]
StrOrStrIterable = Union[str, StrIterable]
BoolOrBoolList = Union[bool, BoolList]
DictOrDictList = Union[dict, DictList]
FloatOrFloatList = Union[float, FloatList]
IntOrIntList = Union[int, IntList]
StrOrStrList = Union[str, StrList]
BoolOrDict = Union[bool, dict]
BoolOrFloat = Union[bool, float]
BoolOrInt = Union[bool, int]
BoolOrStr = Union[bool, str]
DictOrFloat = Union[dict, float]
DictOrInt = Union[dict, int]
DictOrStr = Union[dict, str]
FloatOrInt = Union[float, int]
FloatOrStr = Union[float, str]
IntOrStr = Union[int, str]
Scalar = Union[int, float]
SizedOrIterable = Union[Sized, Iterable]
ArrayLike = Union[ndarray, list]


# matplotlib
ArrowStyle = TypeVar('ArrowStyle', str, ARROW_STYLE)
ArrowStyleIterable = Iterable[ArrowStyle]

BoxStyleTypeIterable = Iterable[BoxStyleType]

CapStyle = TypeVar('CapStyle', str, CAP_STYLE)
CapStyleIterable = Iterable[CapStyle]

Color = TypeVar(
    'Color',
    str,
    Tuple[float, float, float],
    Tuple[float, float, float, float]
)
ColorIterable = Iterable[Color]
ColorOrColorIterable = Union[Color, ColorIterable]

ConnectionStyle = TypeVar('ConnectionStyle', str, CONNECTION_STYLE)
ConnectionStyleIterable = Iterable[ConnectionStyle]

FontSize = TypeVar('FontSize', str, float, int, FONT_SIZE)
FontSizeIterable = Iterable[FontSize]

FontStretch = TypeVar('FontStretch', float, int, FONT_STRETCH)
FontStretchIterable = Iterable[FontStretch]

FontStyle = TypeVar('FontStyle', str, FONT_STYLE)
FontStyleIterable = Iterable[FontStyle]

FontVariant = TypeVar('FontVariant', str, FONT_VARIANT)
FontVariantIterable = Iterable[FontVariant]

FontWeight = TypeVar('FontWeight', int, float, str, FONT_WEIGHT)

JoinStyle = TypeVar('JoinStyle', str, JOIN_STYLE)
JoinStyleIterable = Iterable[JoinStyle]

LegendLocation = TypeVar('LegendLocation', str, Tuple[float, float])

LineStyle = TypeVar('LineStyle', str, LINE_STYLE)
LineStyleIterable = Iterable[LineStyle]

PatchIterable = Iterable[Patch]

PathIterable = Iterable[Path]

PlotObject = TypeVar('PlotObject', Axes, Figure, JointGrid, PairGrid)

StringMapper = Union[Dict[str, str], Callable[[str], str]]
