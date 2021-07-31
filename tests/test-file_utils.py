import setup
from Parser.file_utils import *

path = '../data/Lenna.png'

size = get_file_size(path)
type = get_file_type(path)

last_access = get_last_file_access(path)
last_status_change = get_last_status_change(path)
last_modification = get_last_file_modification(path)

name = get_file_name(path)
extension = get_extension_name(path)

assert size == 473831
assert type == 'regular file'
assert last_access == 'Fri Jul 30 22:50:22 2021\n'
assert last_status_change == 'Fri Jul 30 21:57:44 2021\n'
assert last_modification == 'Fri Jul 30 21:57:44 2021\n'

assert name == 'Lenna'
assert extension == 'png'
