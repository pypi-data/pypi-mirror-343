import matplotlib.pyplot as plt
import numpy as np


def plot():
    fig = plt.figure()
    t = np.arange(5)
    np.random.seed(123)
    x = t
    plt.plot(t, x, label="line")
    plt.scatter(t, x, label="scatter")
    plt.legend()
    return fig


def test():
    from .helpers import assert_equality

    assert_equality(plot, __file__[:-3] + "_reference.tex")
