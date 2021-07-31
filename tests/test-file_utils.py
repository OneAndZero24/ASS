import setup
from Parser.file_utils import *

path = '../data/Lenna.png'

size = get_st_size(path)
type = get_st_mode(path)

last_access = get_st_atime(path)
last_status_change = get_st_ctime(path)
last_modification = get_st_mtime(path)

name = get_filename(path)
extension = get_extension(path)

assert size == 473831
assert type == 'regular file'
#assert last_access == 1627678222
#assert last_status_change == 1627675064
#assert last_modification == 1627675064

assert name == 'Lenna'
assert extension == 'png'
