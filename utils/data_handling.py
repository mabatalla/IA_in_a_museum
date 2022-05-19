"""
Contains the functions used to handle data and raw images
"""
# IMPORTS
import os
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1 import ImageGrid
from pathlib import PurePath

from utils.image_processing import get_img_rgb, resize_img


# FUNCTIONS
def get_collection(path, extensions=None):
    """
    Generate a list with all the paths of archives with a valid extension.

    This function will crawl inside the declared path any file even inside folders and sub folders to check their
    extension. If the extension matches one of the list passed to the function it will add the file path to the
    result.

    Parameters
    ----------
    path : str
        Path to inspect.
    extensions : list
        Extensions to be found.

    Returns
    -------
    collection: list
        Complete paths of the files with a valid extension.
    """
    # Empty list to append valid files path
    collection = []

    # Iterate through the files tree from path
    for path, folders, files in os.walk(path):
        # If image has a valid extension append path to collection
        for name in files:
            file_ext = os.path.splitext(name)[1]

            if file_ext.lower() in extensions:
                collection.append(PurePath(path, name))
            else:
                continue

    return collection


def plot_colors(HEX_indexes, title):
    """

    Parameters
    ----------
    HEX_indexes : list
        Color names in HEX color mode
    title
    sort_colors
    emptycols

    Returns
    -------

    """
    # Get HEX colors names without '#'
    color_names = HEX_indexes

    # Set cell dimensions
    cell_width = 250
    cell_height = 50
    filling_width = 200
    margin = 25
    top_margin = 200

    # Set number of rows
    num_of_colors = len(color_names)
    nrows = num_of_colors

    # Set figure dimensions
    width = cell_width + 2 * margin
    height = cell_height * nrows + margin + top_margin
    dpi = 72

    # Generate figure and axes
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(.1, .1, (width - margin) / width, (height - top_margin) / height)

    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * nrows,
                -cell_height / 2)

    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)

    ax.set_axis_off()

    ax.set_title(title,
                 fontsize=24,
                 loc="left",
                 pad=10)

    for i, color in enumerate(color_names):
        row = i
        col = 1
        y = row * cell_height

        filling_start_x = cell_width * col
        text_pos_x = cell_width * col + filling_width + 7

        ax.text(text_pos_x,
                y + (cell_height / 4),
                color,
                fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')

        ax.add_patch(Rectangle(xy=(filling_start_x, y - 9),
                               width=filling_width,
                               height=40,
                               facecolor=color,
                               edgecolor='0.5'))

    return fig


def rgb_to_hex(color):
    """
    Transform an RGB color into HEX

    Parameters
    ----------
    color : numpy.ndarray
        RGB color reference

    Returns
    -------
    HEX_color : str
        HEX color reference

    """
    HEX_color = f'#{int(color[0]):02x}{int(color[1]):02x}{int(color[2]):02x}'

    return HEX_color


def show_collection(collection):
    """
    Show all images from a collection.

    Parameters
    ----------
    collection: list
        Paths of the files to be shown.
    """
    fig = plt.figure(figsize=(20, 20))

    grid = ImageGrid(fig,
                     111,
                     nrows_ncols=(1, len(collection)) if len(collection) <= 5
                     else ((len(collection) // 5) + 1, 5),
                     axes_pad=0.5)

    for ax, work in zip(grid, collection):
        img_name = str(work).split(sep='/')[-1].split(sep='.')[0]
        ax.set_title(img_name)

        img = get_img_rgb(str(work))
        img_res = resize_img(img, 50)

        ax.imshow(img_res)

    plt.show()

    return None

# VARIABLES


# EXECUTION


# OUTPUT


# END OF FILE
