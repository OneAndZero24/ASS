import setup
from Parser.image_parser import ImageParser

iprs = ImageParser((256, 256))
print(iprs.parse("../data/Lenna.png"))