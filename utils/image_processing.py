"""
Contains the functions used to process raw images for ML algorithms
"""
# IMPORTS
import cv2
import matplotlib.pyplot as plt
import numpy as np

from collections import Counter
from matplotlib.patches import Rectangle
from sklearn.cluster import KMeans


# FUNCTIONS
def color_clustering(image, color_mode='HEX', bins=5, num_of_colors=10, show_chart=True):
    """
    Extract a number of colors from an image.

    This function applies a color quantization based on cv2.kmeans function
    as described in the OpenCV docs to reduce the colors present on an image.

    Parameters
    ----------
    image : numpy.ndarray
        Image to extract color from
    color_mode : str
        Color mode to return colors (RGB, HEX)
    bins : int
        Number of possible values for each RGB channel
    num_of_colors : int
        Number of clusters
    show_chart : bool
        Whether to show a chart with found colors

    Returns
    -------
    colors : list
        List of colors in specified color mode
    """
    # Collapse image into one dimension (KMeans requirement)
    img = image.reshape(image.shape[0]*image.shape[1], 3)

    # Use KMeans to generate num_of_colors number of clusters
    model_kmeans = KMeans(n_clusters=num_of_colors)
    labels = model_kmeans.fit_predict(img)  # This returns a number of cluster for each pixel
    color_clusters = model_kmeans.cluster_centers_  # This are the RGB values of the centroids

    # Transform color clusters to a discrete variable and its type to list
    color_clusters = np.array(color_clusters)  # Needed for reduce_col_palette
    color_clusters = reduce_col_palette(np.array(color_clusters), bins=bins)
    color_clusters = color_clusters.tolist()
    # color_clusters = color_clusters.round().tolist()

    # Count and sort the pixels in each cluster to order colors by most common
    color_counts = Counter(labels)  # Get color as keys and counts as values
    color_counts = color_counts.most_common()  # Order color by counts

    # Get RGB and HEX indexes
    ordered_RGB_colors = [color_clusters[i[0]] for i in color_counts]
    ordered_HEX_colors = [rgb_to_hex(i).upper() for i in ordered_RGB_colors]

    if show_chart:
        plot_colors(ordered_HEX_colors)
        plt.show()

    if color_mode == 'RGB':
        colors = ordered_RGB_colors

    else:
        colors = ordered_HEX_colors

    return color_clusters


def get_img_rgb(image_path):
    """
    Import image in RGB mode.

    By default, OpenCV reads image in BGR color mode so we need to convert it to RGB.

    Parameters
    ----------
    image_path : str
        Path of the image

    Returns
    -------
    image : numpy.ndarray
        Image in RGB color mode
    """
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img


def map_channel(channel_value, bins):
    """
    Map an RGB channel value (0 to 255) to a limited options.

    The number of bins sets the number of possible values that the channel can
    get.

    Parameters
    ----------
    channel_value : int
        Value of one channel
    bins : int
        Number of posible values

    Returns
    -------
    mapped_value : int
        New value for the channel

    Examples
    --------
    >>> R_px = 200
    ... map_channel(R_px, 3)
    255

    >>> G_px = 140
    ... map_channel(G_px, 3)
    127

    >>> B_px = 150
    ... map_channel(B_px, 3)
    127
    """
    if channel_value >= 255:
        mapped_value = 255
    else:
        preprocessed_value = np.floor((channel_value*bins)/255)
        mapped_value = abs(int(preprocessed_value*(255/(bins - 1))))

    return mapped_value


def reduce_col_palette(image, bins, info=False):
    """
    Map all pixels of an image to a reduced palette.

    This function iterates through every pixel of an image to map each
    color to a reduced palette.

    In standard RGB color mode, every channel has a value between 0 and 255.
    This results in 256x256x256 colors, this is more than 16M.

    This function reduces the possibilities of every channel to the number
    passed as bins.

    Parameters
    ----------
    image : numpy.ndarray
        Image to reduce color palette
    bins : int
        Number of possible values for each RGB channel
    info : bool
        Whether to inform the user the result

    Returns
    -------
    img : numpy.ndarray
        Image with a reduced color palette
    """
    # Collapse image into one dimension
    img = image.flatten()

    # Iterate the array to transform the value of each channel in the pixels
    for i, channel_val in enumerate(img):
        if channel_val == 255:
            img[i] = 255
        else:
            img[i] = map_channel(channel_val, bins)

    # Restore image shape
    img = np.reshape(img, image.shape)

    # Inform user
    if info:
        print(f'Palette reduced to {bins ** 3} colors.')

    return img


def resize_img(image, height):
    """
    Resize image keeping ratio.

    Parameters
    ----------
    image : numpy.ndarray
        Image to resize
    height : int
        Desired height in pixels

    Returns
    -------
    img : numpy.ndarray
        Image with desired height and original ratio
    """
    ratio = image.shape[0]/image.shape[1]
    width = int(height/ratio)

    return cv2.resize(image, dsize=(width, height), interpolation=cv2.INTER_AREA)


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


def square_img(image, height):
    """
    Resize image to a square ratio.

    Parameters
    ----------
    image : numpy.ndarray
        Image to resize
    height : int
        Desired height in pixels

    Returns
    -------
    img_sqr : numpy.ndarray
        Image with desired height and squared ratio
    """
    img = cv2.resize(image, (height, height), interpolation=cv2.INTER_AREA)

    return img


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


# VARIABLES


# EXECUTION


# OUTPUT


# END OF FILE
