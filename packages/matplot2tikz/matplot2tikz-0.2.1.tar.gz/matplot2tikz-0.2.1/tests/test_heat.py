import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def plot():
    fig = plt.figure()
    x, y = np.ogrid[-10:10:100j, -10:10:100j]
    extent = (x.min(), x.max(), y.min(), y.max())
    cmap = matplotlib.colormaps.get_cmap("gray")
    plt.imshow(x * y, extent=extent, cmap=cmap)
    plt.colorbar()
    return fig


def test():
    from .helpers import assert_equality

    assert_equality(plot, "test_heat_reference.tex")
