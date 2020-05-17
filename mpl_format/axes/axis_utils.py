import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def new_axes(width: int = 16, height: int = 9) -> Axes:
    """
    Return new matplotlib axes.
    """
    _, ax = plt.subplots(figsize=(width, height))
    return ax
