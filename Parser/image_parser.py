import numpy as np
from PIL import Image

class ImageParser:
    def __init__(self):
        pass
        
    def parse(self, path, size):
        arr = None
        with Image.open(path).convert("RGB") as img:
            img = img.resize(size)
            arr = np.array(img)
            img.show()
        return arr.flatten()