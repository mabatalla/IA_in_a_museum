"""
Contains the functions used to prepare raw images for ML algorithms
"""

# IMPORTS
# from cv2 import COLOR_BGR2RGB, cvtColor, INTER_AREA, imread, resize
import cv2


# FUNCTIONS
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
    image : TODO
        Image in RGB color mode

    """
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img


def resize_img(image, height):
    """
    Resize image keeping ratio.

    Parameters
    ----------
    image : TODO

    height : int
        Desired height in pixels

    Returns
    -------
    img : TODO
        Image with desired height and original ratio
    """
    ratio = image.shape[0]/image.shape[1]
    width = int(height/ratio)

    return cv2.resize(image, dsize=(width, height), interpolation=cv2.INTER_AREA)


def square_img(image, height):
    """
    Resize image to a square ratio.

    Parameters
    ----------
    image : TODO

    height : int
        Desired height in pixels

    Returns
    -------
    img_sqr : TODO
        Image with desired height and squared ratio
    """

    img = cv2.resize(image, (height, height), interpolation=cv2.INTER_AREA)

    return img

# VARIABLES


# EXECUTION


# OUTPUT


# END OF FILE
