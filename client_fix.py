import file
from packet import *
from file import File
import socket
import const
import pickle
import time
from progressbar import *

progress_bar = ProgressBar()

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect((socket.gethostname(), const.SERVER_PORT))

test_file_path = '{}/test.zip'.format(file.get_current_directory())
test_file_obj = File(test_file_path)

chunk_generator = test_file_obj.get_chunks_generator()
num_of_chunk = test_file_obj.calculate_chunks_number()

packet_class = Packet(1)

new = open('lala.zip', 'ab')

counter = 0
progress_bar.set_total(num_of_chunk)
for chunk in chunk_generator:
    packet = packet_class.create_packet(chunk)
    # s.send(packet)
    # ack = s.recv(1)

    new_chunk = packet_class.read_packet_from_bytes_array(packet)

    counter += 1
    progress_bar.printProgressBar(counter)

    new.write(new_chunk)

    # send file to server
    # receive acknowledgement from server

print(counter)