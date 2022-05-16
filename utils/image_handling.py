"""
Contains the functions used to prepare raw images for ML algorithms
"""

# IMPORTS
import cv2


# FUNCTIONS
def resize_img(image, height):
    """
    Resize image keeping ratio.

    Parameters
    ----------
    image: str
    height

    Returns
    -------

    """
    ratio = image.shape[0]/image.shape[1]
    width = int(height/ratio)

    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

# VARIABLES


# EXECUTION


# OUTPUT


# END OF FILE
