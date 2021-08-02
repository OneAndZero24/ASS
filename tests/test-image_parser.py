import setup
from Parser.image_parser import ImageParser

print("\nTEST: " + __file__)

iprs = ImageParser((4, 4))
arr, img_data, gps_data, exif_offset_data = iprs.parse("../data/Lenna.png")

print("arr:")
print(arr)
print("img data:")
print(img_data)
print("gps data:")
print(gps_data)
print("exif_offset_data:")
print(exif_offset_data)