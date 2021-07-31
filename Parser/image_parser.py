import numpy as np
from PIL import Image

class ImageParser(Parser):
    def __init__(self, size):
        self.size = size
        pass
        
    def parse(self, path):
        arr = None
        with Image.open(path).convert("RGB") as img:
            img = img.resize(self.size)
            arr = np.array(img)
        return arr.flatten()