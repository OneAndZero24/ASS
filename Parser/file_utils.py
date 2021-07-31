import ctypes
shared_lib = None

def load_shared_library():
    path = __file__
    path = path.replace('file_utils.py', 'metadata.so')
    return ctypes.CDLL(path)

def get_st_mode(path):
    global shared_lib
    
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_st_mode = shared_lib.getFileType
    c_get_st_mode.restype = ctypes.c_char_p
    c_get_st_mode.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_st_mode(path).decode('utf-8')

def get_st_atime(path): # last file access
    global shared_lib
    
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_st_atime = shared_lib.getLastFileAccess
    c_get_st_atime.restype = ctypes.c_longlong
    c_get_st_atime.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_st_atime(path)

def get_st_ctime(path): # last status change
    global shared_lib
    
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_st_ctime = shared_lib.getLastStatusChange
    c_get_st_ctime.restype = ctypes.c_longlong
    c_get_st_ctime.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_st_ctime(path)

def get_st_mtime(path): # last modification time
    global shared_lib
    
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_st_mtime = shared_lib.getLastFileModification
    c_get_st_mtime.restype = ctypes.c_longlong
    c_get_st_mtime.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_st_mtime(path)

def get_st_size(path):    # size in bytes
    global shared_lib
    
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_st_size = shared_lib.getFileSize
    c_get_st_size.restype = ctypes.c_longlong
    c_get_st_size.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_st_size(path)

def get_file_name(path):
    name = path.split('/')[-1]
    if '.' in name:
        return name.split('.')[0]
    else:
        return name

def get_extension_name(path):
    name = path.split('/')[-1]
    if '.' in name:
        return name.split('.')[1]
    else:
        return None