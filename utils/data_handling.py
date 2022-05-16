"""
Contains the functions used to handle data and raw images
"""

# IMPORTS
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

from mpl_toolkits.axes_grid1 import ImageGrid
from pathlib import PurePath

from utils.image_handling import resize_img


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


# To show all images from a collection
def show_collection(collection, cols=5):
    """
    Show all images from a collection.

    Parameters
    ----------
    collection: list
        Paths of the files to be shown.
    cols : int
        Columns in the figure shown.

    """
    
    fig = plt.figure(figsize=(20, 20))

    if len(collection) < 5:
        grid_dims = (1, len(collection))

    elif len(collection) > 5:
        grid_dims = ((len(collection)//cols) + 1, 5)

    grid = ImageGrid(fig,
                     111,
                     nrows_ncols=grid_dims,
                     axes_pad=0.5)

    for ax, work in zip(grid, collection):
        img_name = str(work).split(sep='/')[-1].split(sep='.')[0]
        ax.set_title(img_name)

        img = mpimg.imread(str(work))
        img_res = resize_img(img, 50)

        ax.imshow(img_res)

    plt.show()

    return None

# VARIABLES


# EXECUTION


# OUTPUT


# END OF FILE
