import struct
import socket
import const
import os
from pathlib import Path
from math import floor, ceil

EIGHT_KB = 8;

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((socket.gethostname(), const.SERVER_PORT))

def readFileInChunks(file_object, chunk_size = EIGHT_KB):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 8bytes"""

    num_of_chunk = calculate_chunks_number(file_object, chunk_size)

    for i in range(num_of_chunk):
        data = file_object.read(chunk_size)
        yield data

def calculate_chunks_number(file_object, chunk_size = EIGHT_KB):
    file_size = os.fstat(file_object.fileno()).st_size
    num_of_chunk = ceil(file_size/chunk_size)
    return num_of_chunk


home = Path.home()

f = open("{}/Downloads/source-sans-pro.zip".format(home), "rb")

print(calculate_chunks_number(f))
a = 0

for piece in readFileInChunks(f):
    a+=1

print(a)

# while True:
#     msg = s.recv(8)
#     print(msg.decode("utf-8"))


