import setup
from Parser.file_utils import *
from PIL import Image

print("\nTEST" + __file__)

def display_dict(dictionary):
    """displays dictionary as list with 2 columns for keys and values"""

    for key, value in dictionary.items():
        print(str(key) + ': \t' + str(value))

path = '../data/Lenna.png'

size = get_st_size(path)
type = get_st_mode(path)

last_access = get_st_atime(path)
last_status_change = get_st_ctime(path)
last_modification = get_st_mtime(path)

name = get_filename(path)
extension = get_extension(path)


# basic assertions to verify correctnes of functions derived from metadata.c
assert size == 473831
assert type == 'regular file'
assert name == 'Lenna'
assert extension == 'png'


path = '../data/DSCN0010.jpg'

# function to obtain various image metadata
image = Image.open(path)
img, gps, offset = get_image_metadata(image)

del offset['MakerNote']
print("\n=====Image metadata:=====\n")
display_dict(img)
print("\n=====GPS metadata:=====\n")
display_dict(gps)
print('\n====ExifOffset metadata:=====\n')
display_dict(offset)