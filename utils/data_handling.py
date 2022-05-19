"""
Contains the functions used to handle data
"""
# IMPORTS
import os
import matplotlib.pyplot as plt

from csv import writer
from cv2 import COLOR_RGB2BGR, cvtColor
from cv2 import imwrite as save_img
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1 import ImageGrid
from pathlib import PurePath

from utils.image_processing import get_img_rgb
from utils.image_processing import square_img
from utils.image_processing import reduce_col_palette
from utils.image_processing import resize_img

from utils.misc import infinite_sequence


# FUNCTIONS
def process_collection(collection,
                       resize_height=150,
                       label='new_label',
                       save=False,
                       save_path=False):
    """
    Process images of a collection and extracts color data.

    Parameters
    ----------
    collection : list
        List with paths to images
    resize_height : int
        Desired height in pixels
    label : str
        Label for the images and data
    save : bool
        Whether to save data and images
    save_path: str
        Path in which save data and images

    Returns
    -------
    collection_data : list
        List of features extracted

    errors_log : list
        List of files that raised an exception
    """
    collection_data = []
    errors = 0
    errors_log = []
    index = infinite_sequence()

    if save:
        # Set origin dir
        origin_dir = os.getcwd()

        if save_path:
            # Move to save_path
            os.chdir(save_path)

        # Create new dir
        os.mkdir(label)

    for img in collection:
        img_path = str(img)
        img_name = img_path.split(sep='/')[-1].split(sep='.')[0]

        try:
            # Get image RGB and resize
            img = get_img_rgb(img)
            img = resize_img(img, resize_height)

            # Get ratio
            dim_ratio = round(img.shape[0] / img.shape[1], ndigits=5)

            # Resize to reduce_col_palette and color_clustering
            img = square_img(img, 150)
            img = reduce_col_palette(img, 5)

            # Get color features
            chiaroscuro, whitespace_ratio = get_color_features(img)

            # Gather image data
            img_data = [label, img_name, dim_ratio, chiaroscuro, whitespace_ratio]

            # Add img_data to collection_data
            collection_data.append(img_data)

            if save:
                # Revert img to BGR before saving
                img_to_save = cvtColor(img, COLOR_RGB2BGR)

                # Save image
                save_img(f'{os.getcwd()}/{label}/{img_name}_{str(next(index))}', img_to_save)

        except (BaseException, Exception):
            errors += 1
            errors_log.append(img_name)
            continue

    if save:
        # Save collection data
        with open(f'{os.getcwd()}/{label}/{label}.csv', "w", newline="") as file:
            quill = writer(file)
            quill.writerows(collection_data)

        # Go back to origin dir
        os.chdir(origin_dir)

    # Inform user
    print(f'{errors} exceptions raised during the process. Check errors_log for more info.')

    return collection_data, errors_log


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

    print(f'{len(collection)} images found')

    return collection


def get_color_features(image):
    """
    Extract color features from one image.

    Parameters
    ----------
    image

    Returns
    -------

    """
    img = image

    # Set color counter
    black_px = 0
    white_px = 0
    color_px = 0

    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            if (img[row][col] <= 50).all():
                black_px += 1
            elif (img[row][col] >= 206).all():
                white_px += 1
            else:
                color_px += 1

    chiaroscuro = round(white_px / black_px, ndigits=5)
    whitespace_ratio = round((white_px * 100) / (img.size // 3), ndigits=5)

    return chiaroscuro, whitespace_ratio


def plot_colors(HEX_indexes):
    """
    Plot a color chart in order of importance

    Parameters
    ----------
    HEX_indexes : list
        Color names in HEX color mode

    Returns
    -------
    fig : Figure
        Color chart
    """
    # Get HEX colors names without '#'
    color_names = HEX_indexes

    # Set cell dimensions
    cell_width = 200
    cell_height = 50
    filling_width = 300
    margin = 5

    # Set number of rows
    num_of_colors = len(color_names)
    nrows = num_of_colors

    # Set figure dimensions
    width = cell_width + 2 * margin
    height = cell_height * nrows
    dpi = 72

    # Generate figure and axes
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi),
                           dpi=dpi)

    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * nrows,
                -cell_height / 2)

    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)

    ax.set_axis_off()

    ax.set_title('Colors found (ordered)',
                 fontsize=20,
                 loc="center",
                 pad=-5)

    for i, color in enumerate(color_names):
        row = i
        # col = 1
        y = row * cell_height

        filling_start_x = 5
        text_pos_x = filling_start_x + filling_width + 50

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
                               edgecolor='0'))

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
