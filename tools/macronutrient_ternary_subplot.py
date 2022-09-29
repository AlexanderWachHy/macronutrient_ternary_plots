# Author: A.Wachholz
# Date: 29.09.22


# imports
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mc
import ternary


# set random seed
np.random.seed(42)

# define constants
FS = 14

# define functions


def draw_ticks(tax, fs, tick_locs=range(10, 100, 10)):
    """

    :param tax:
    :param fs:
    :param tick_locs:
    :return: manually draws roatated ticks matching the rotation of the
    corresponding axis
    """

    # add left ticks
    for i in tick_locs:
        tax.annotate(
            text=str(i),
            position=[-10, 100-i +2, 90],
            rotation=300,
            fontsize=fs
        )
        # add tick lines
        tax.line(
            [-3 , i+3, 90],
            [0 , i, 90],
            color='k'
        )

    # add bottom ticks
    for i in tick_locs:
        tax.annotate(
            text=str(i),
            position=[i - 2, -10, 90],
            rotation=60,
            fontsize=fs
        )
        # add tick lines
        tax.line(
            [i, -3, 90],
            [i, 0, 90],
            color='k'
        )

    # add right ticks
    for i in tick_locs:
        tax.annotate(
            text=str(i),
            position=[105-i, i-2, 0],
            rotation=0,
            fontsize=fs
        )
        # add tick lines
        tax.line(
            [100-i , i, 0],
            [103-i , i, 0],
            color='k'
        )


def ternary_subplot(
        ax,
        fs,
        blbl='$NO3-N_{r}$',
        rlbl='$TOC_{r}$',
        llbl='$PO4-P_{r}$',
        offset=.15,
        b_offset=.1
):
    """

    :param ax: mpl subplot object
    :param fs: fontsize int
    :param blbl: bottom label str
    :param rlbl: right label str
    :param llbl: left label str
    :return:
    """

    # create ternary subplot
    tax = ternary.TernaryAxesSubplot(ax=ax, scale=100)

    # draw Boundary
    tax.boundary(linewidth=2.0)

    # draw grid
    tax.gridlines(color="black", multiple=10)

    # draw ticks
    draw_ticks(tax=tax, fs=fs)

    # add labels
    tax.left_axis_label(llbl, fontsize=fs+2, offset=offset)
    tax.right_axis_label(rlbl, fontsize=fs+2, offset=offset)
    tax.bottom_axis_label(blbl, fontsize=fs+2, offset=b_offset)
    tax._redraw_labels()
    tax.ax.set_aspect('equal', adjustable='box')

    # draw center
    tax.scatter([[100/3, 100/3, 100/3]], color='k', marker='o', s=60)

    # remove mpl axes
    tax.clear_matplotlib_ticks()
    tax.get_axes().axis('off')

    # return ternary subplot
    return tax


def add_cbar(sc, ax, cmap, ticks, tick_labels, fs, label, aspect=7, shrink=.5):
    """

    :param sc: pyplot scatter obj on ternary sub plot
    :param ax: ax from which ternary suplods tax was created
    :param cmap: mpl color map str
    :param ticks: list of ticks as fraction of 1
    :param tick_labels: labels for ticks
    :param aspect: aspect ratio of cbar
    :param fs: fontsize of tick labels anb label
    :param label: title of cbars y axis
    :param shrink: reduction of vertical extent as fraction of vertical axis extent
    :return:
    """

    cb = sc.figure.colorbar(
        # on the fly creation of mappable
        ax=ax,
        mappable=cm.ScalarMappable(norm=None, cmap=cmap),
        orientation='vertical',
        # shrink vertical
        shrink=shrink,
        ticks=ticks,
        # increase width
        aspect=aspect
    )
    cb.ax.set_yticklabels(
        tick_labels,
        fontsize=fs
    )
    cb.set_label(label=label, fontsize=FS)


if __name__ == "__main__":

    # define fig and ax
    figure, ax = plt.subplots(figsize=(6, 6))

    # create ternary subplot
    tax = ternary_subplot(
        ax=ax,
        fs=FS,
        llbl='left label',
        rlbl='right label',
        blbl='bottom label',
        #offset=.15,
        #b_offset=.1
    )

    # draw lines
    tax.plot([[10, 80, 10], [80, 10, 10]], linestyle='--', color='r')
    tax.plot([[10, 10, 80], [80, 10, 10]], linestyle='--', color='r')
    tax.plot(
        [[10, 10, 80], [10, 80, 10]],
        linestyle='--',
        color='r',
        label='some lines'
    )

    # generate some random data_storage for scatter plots
    bottom = np.random.randint(0, 33, 10)
    left = np.random.randint(0, 50, 10)
    right = 100 - (bottom + left)
    color = range(10)
    data = pd.DataFrame(zip(bottom, left, right))

    # draw scatter plot
    scatter = tax.scatter(
        np.asarray(data[[0, 1, 2]]),
        c=color,
        vmin=0,
        vmax=10,
        cmap='Blues',
        label='some data_storage'
    )

    # draw cbar
    add_cbar(
        sc=scatter,
        ax=ax,
        cmap='Blues',
        ticks=[0, .2, .4, .6, .8, 1],
        tick_labels=[0, 2, 4, 6, 8, 10],
        fs=FS,
        label='cbar label'
    )

    # draw legend
    leg = ax.legend(
        loc='upper left',
        fontsize=FS,
    )
    leg.set_title(
        'legend title',
        prop={'size': FS}
    )
    plt.tight_layout()
    plt.show()

