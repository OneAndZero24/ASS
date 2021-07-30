from PIL import Image
import numpy as np

class ImgParser:
    def __init__(self):
        pass
        
    def parse(self, path, size):
        arr = None
        with Image.open(path).convert("RGB") as img:
            img = img.resize(size)
            arr = np.array(img)
        return arr