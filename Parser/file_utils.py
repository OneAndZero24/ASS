import ctypes
from PIL import Image, ExifTags

shared_lib = None #stores CDLL object

"""
Set of functions that obtain metadata directly from path or from stat struct(POSIX)
"""

def load_shared_library():
    """loads shared library metadata.c which provides set of functions that obtain data from stat structure"""

    path = __file__
    path = path.replace('file_utils.py', 'metadata.so')
    return ctypes.CDLL(path)

def get_st_mode(path):
    """returns type of file(ordinary file, directory, fifo/pipe etc..."""

    global shared_lib
    
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_st_mode = shared_lib.getFileType
    c_get_st_mode.restype = ctypes.c_char_p
    c_get_st_mode.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_st_mode(path).decode('utf-8')

def get_st_atime(path):
    """returns last file access(as integer)"""

    global shared_lib
    
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_st_atime = shared_lib.getLastFileAccess
    c_get_st_atime.restype = ctypes.c_longlong
    c_get_st_atime.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_st_atime(path)

def get_st_ctime(path):
    """returns last status change(as integer)"""

    global shared_lib
    
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_st_ctime = shared_lib.getLastStatusChange
    c_get_st_ctime.restype = ctypes.c_longlong
    c_get_st_ctime.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_st_ctime(path)

def get_st_mtime(path):
    """returns last modification time"""

    global shared_lib
    
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_st_mtime = shared_lib.getLastFileModification
    c_get_st_mtime.restype = ctypes.c_longlong
    c_get_st_mtime.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_st_mtime(path)

def get_st_size(path):
    """returns size of file(in bytes)"""

    global shared_lib
    
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_st_size = shared_lib.getFileSize
    c_get_st_size.restype = ctypes.c_longlong
    c_get_st_size.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_st_size(path)

def get_filename(path):
    """returns filename(if filename includes extension it will be removed)"""
    name = path.split('/')[-1]
    if '.' in name:
        return name.split('.')[0]
    else:
        return name

def get_extension(path):
    """return extension(if filename do not include extension it will return None)"""
    name = path.split('/')[-1]
    if '.' in name:
        return name.split('.')[1]
    else:
        return None

"""
Functions dedicated for extracting metadata from images
"""

def get_image_metadata(image):
    """
    Returns dictionary with all image metadata(EXIF is writeable so values might be wrong)

    Keyword arguments:
    image - a PIL Image object
    """

    exifdata = image.getexif()

    img_data = dict()
    gps_data = dict()
    exif_offset_data = dict()

    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = ExifTags.TAGS.get(tag_id, tag_id)

        # old way of obtaining GPSInfo was deprecated in PIL 8.2.0
        # now it can be obtained via exifdata.get_ifd(0x8825)
        # where 0x8825 is equivalent of GPSInfo
        # same goes for ExifOffset(0x8769)
        # more details in Pillow documentation and Pillow/ExifTags.py

        if tag_id == 0x8825: # GPSInfo
            for key, value in exifdata.get_ifd(0x8825).items():
                gps_tag = ExifTags.GPSTAGS.get(key,key)

                if isinstance(value, bytes):
                    try:
                        decoded = value.decode()
                        value = decoded
                    except Exception as e:
                        pass
                gps_data[gps_tag] = value
        elif tag_id == 0x8769: # ExifOffset
            for key, value in exifdata.get_ifd(0x8769).items():
                exif_offset_tag = ExifTags.TAGS.get(key,key)

                if isinstance(value, bytes):
                    try:
                        decoded = value.decode()
                        value = decoded
                    except Exception as e:
                        pass
                exif_offset_data[exif_offset_tag] = value
        else: # basic image metadata
            data = exifdata.get(tag_id)
            # decode bytes 
            if isinstance(data, bytes):
                try:
                    decoded = data.decode()
                    data = decoded
                except Exception as e:
                    pass
            img_data[tag] = data
    
    return (img_data, gps_data, exif_offset_data)