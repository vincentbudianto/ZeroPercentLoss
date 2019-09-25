import os
from pathlib import Path
from const import *

from math import floor, ceil

HOME = Path.home()

def get_current_directory():
    current_directory = os.getcwd()
    return current_directory

def create_folder(folder_name):
    current_directory = get_current_directory()
    folder_directory_path = "{}/{}".format(current_directory, folder_name)
    if not os.path.exists(folder_directory_path):
        os.makedirs(folder_directory_path)
    return folder_directory_path

def get_source_directory():
    return create_folder('source')

def get_destination_directory():
    return create_folder('destination')

class File:
    def __init__(self, file_path):
        self.file_path = file_path
        self.open_file_read_binary_mode(self.file_path)

    def open_file_read_binary_mode(self, path):
        self.file = open(path, "rb")

    # return total chunk of a file
    def calculate_chunks_number(self, chunk_size = THIRTYTWO_KB):
        file_size = os.fstat(self.file.fileno()).st_size
        num_of_chunk = ceil(file_size/chunk_size)
        return num_of_chunk

    # return generator
    def get_chunks_generator(self, chunk_size = THIRTYTWO_KB):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 8kb"""

        num_of_chunk = self.calculate_chunks_number()

        for i in range(num_of_chunk):
            data = self.file.read(chunk_size)
            yield data