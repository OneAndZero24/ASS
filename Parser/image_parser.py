import numpy as np
from PIL import Image
from .parser_baseclass import Parser
from .file_utils import get_image_metadata

class ImageParser(Parser):

    """
    Basically ImageParser focuses only on data characteristic for images 
    such as information described in Exif standard
    and image itself(values of pixels)
    """

    def __init__(self, size):

        """
        Keyword arguments:
        size - (int, int) tuple with dimensions of image after resizing
        """

        self.size = size
        
    def parse(self, path):

        """
        Return value:
        (arr,img_data,gps_data,exif_offset_data) where:

        arr - ndarray

        img_data, gps_data, exif_offset_data - dict

        Keyword arguments:
        path - str object that stores path to image
        """

        arr = None

        img_data = None
        gps_data = None
        exif_offset_data = None

        with Image.open(path) as img:
            img_data, gps_data, exif_offset_data = get_image_metadata(img)
            img = img.convert("RGB")
            img = img.resize(self.size)
            arr = np.array(img)

        return (arr, img_data, gps_data, exif_offset_data)