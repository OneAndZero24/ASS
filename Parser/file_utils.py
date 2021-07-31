import ctypes
shared_lib = None

def load_shared_library():
    path = __file__
    path = path.replace('file_utils.py', 'metadata.so')
    print(path)
    return ctypes.CDLL(path)

def get_file_type(path, shared_lib):
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_file_type = shared_lib.getFileType
    c_get_file_type.restype = ctypes.c_char_p
    c_get_file_type.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_file_type(path).decode('utf-8')

def get_last_file_access(path, shared_lib):
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_last_file_access = shared_lib.getLastFileAccess
    c_get_last_file_access.restype = ctypes.c_char_p
    c_get_last_file_access.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_last_file_access(path).decode('utf-8')

def get_last_status_change(path, shared_lib):
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_last_status_change = shared_lib.getLastStatusChange
    c_get_last_status_change.restype = ctypes.c_char_p
    c_get_last_status_change.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_last_status_change(path).decode('utf-8')

def get_last_file_modification(path, shared_lib):
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_last_file_modification = shared_lib.getLastFileModification
    c_get_last_file_modification.restype = ctypes.c_char_p
    c_get_last_file_modification.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_last_file_modification(path).decode('utf-8')

def get_file_size(path, shared_lib):    #Size in bytes
    if not shared_lib:
        shared_lib = load_shared_library()

    c_get_file_size = shared_lib.getFileSize
    c_get_file_size.restype = ctypes.c_longlong
    c_get_file_size.argtypes = [ctypes.c_char_p]

    path = path.encode('utf-8')
    return c_get_file_size(path)

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