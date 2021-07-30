from imgParser import ImgParser
import os
import ctypes


def load_shared_library():
    path = __file__
    path = path.replace('parser.py','metadata.so')
    return ctypes.CDLL(path)

def get_file_type(path,shared_lib):
    c_get_file_type = shared_lib.getFileType
    c_get_file_type.restype = ctypes.c_char_p
    c_get_file_type.argtypes = [ ctypes.c_char_p ]

    path = path.encode('utf-8')
    return c_get_file_type(path).decode('utf-8')

def get_last_file_access(path,shared_lib):
    c_get_last_file_access = shared_lib.getLastFileAccess
    c_get_last_file_access.restype = ctypes.c_char_p
    c_get_last_file_access.argtypes = [ ctypes.c_char_p ]

    path = path.encode('utf-8')
    return c_get_last_file_access(path).decode('utf-8')

def get_last_status_change(path,shared_lib):
    c_get_last_status_change = shared_lib.getLastStatusChange
    c_get_last_status_change.restype = ctypes.c_char_p
    c_get_last_status_change.argtypes = [ ctypes.c_char_p ]

    path = path.encode('utf-8')
    return c_get_last_status_change(path).decode('utf-8')

def get_last_file_modification(path,shared_lib):
    c_get_last_file_modification = shared_lib.getLastFileModification
    c_get_last_file_modification.restype = ctypes.c_char_p
    c_get_last_file_modification.argtypes = [ ctypes.c_char_p ]

    path = path.encode('utf-8')
    return c_get_last_file_modification(path).decode('utf-8')

class Parser:

    def __init__(self):
        self.shared_lib = load_shared_library()

    def parse(self,directory):
        print( get_file_type(directory,self.shared_lib) )
        print( get_last_file_access(directory,self.shared_lib) )
        print( get_last_status_change(directory,self.shared_lib) )
        print( get_last_file_modification(directory,self.shared_lib) )


p = Parser()
p.parse('/Users/mr/ASS/Parser/file.txt')