"""
Contains the functions used to handle data
"""
# IMPORTS
import os
from csv import writer
from pathlib import PurePath

import matplotlib.pyplot as plt
from cv2 import COLOR_RGB2BGR, cvtColor, imwrite as save_img
from mpl_toolkits.axes_grid1 import ImageGrid

from utils.image_processing import color_clustering, get_img_rgb, reduce_col_palette, resize_img, square_img
from utils.misc import infinite_sequence


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
    # Get last folder name
    folder = path.split('/')[-1]

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

    print(f'{len(collection)} images found in {folder}')

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

    chiaroscuro = round(white_px/black_px, ndigits=5)
    whitespace_ratio = round((white_px*100)/(img.size//3), ndigits=5)

    return chiaroscuro, whitespace_ratio


def process_collection(collection,
                       resize_height=150,
                       color_mode='HEX',
                       label='new_label',
                       save=False,
                       save_path=False):
    """
    Process images of a collection and extracts color data.

    If you specify a save_path this function will create a new folder named "label" in that folder. The folder
    shouldn't exists.

    Parameters
    ----------
    collection : list
        List with paths to images
    resize_height : int
        Desired height in pixels
    color_mode:
        Whether to use RGB or HEX color mode
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
        try:
            # Get origin dir
            origin_dir = os.getcwd()

            if save_path:
                # Move to save_path
                os.chdir(save_path)

                # Create new dir
                os.mkdir(label)

                # Set saving dir
                save_dir = save_path + f'/{label}'

                # Go back to origin dir
                os.chdir(origin_dir)

            else:
                # Create new dir
                os.mkdir(label)

                # Set saving dir
                save_dir = origin_dir + f'/{label}'

        except FileExistsError:
            os.chdir(origin_dir)

            return print(f'FileExistsError: "{label}" folder already exists in your saving path.'), \
                   print("Remove it or type a different label name.\n")

    for img in collection:
        img_path = str(img)
        img_name = label + '_' + str(next(index))
        img_extension = img_path.split(sep='/')[-1].split(sep='.')[-1]

        try:
            # Get image RGB and resize
            img = get_img_rgb(img_path)
            img = resize_img(img, resize_height)

            # Get ratio
            dim_ratio = round(img.shape[0]/img.shape[1], ndigits=5)

            # Resize to reduce_col_palette and color_clustering
            img = square_img(img, 150)
            img = reduce_col_palette(img, 5)

            # Get color features
            chiaroscuro, whitespace_ratio = get_color_features(img)

            # Apply color clustering
            colors = color_clustering(img, color_mode=color_mode, num_of_colors=5, show_chart=False)

            # Gather image data
            img_data = [label, img_name, dim_ratio, chiaroscuro, whitespace_ratio]
            for i in colors:
                img_data.append(i)

            # Add img_data to collection_data
            collection_data.append(img_data)

            if save:
                # Revert img to BGR before saving
                img_to_save = cvtColor(img, COLOR_RGB2BGR)

                # Save image
                filename = img_name + '.' + img_extension
                save_img(f'{save_dir}/{filename}', img_to_save)

        except (BaseException, Exception):
            errors += 1
            errors_log.append(img_name)
            continue

    if save:
        # Save collection data
        with open(f'{save_dir}/{label}.csv', "w", newline="") as file:
            quill = writer(file)
            quill.writerows(collection_data)

    # Inform user
    print(f'{errors} exceptions raised during the process. Check errors_log for more info.\n')

    return collection_data, errors_log


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
                     else ((len(collection)//5) + 1, 5),
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
