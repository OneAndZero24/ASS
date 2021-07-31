import setup
from Parser.file_utils import get_file_size

path = '../data/Lenna.png'

size = get_file_size(path)
print(size)


