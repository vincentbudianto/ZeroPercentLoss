from packet import *
from file import File
from progressbar import *
import const
import file
import multiprocessing
import pickle
import socket
import time
import sys

progress_bar = ProgressBar()

def send_thread(filename, client_address, clientSocket):
    counter = 0

    path = '{}/' + filename
    file_path = path.format(file.get_source_directory())
    file_obj = File(file_path)

    chunk_generator = file_obj.get_chunks_generator()
    num_of_chunk = file_obj.calculate_chunks_number()

    packet_class = Packet(counter)
    progress_bar.set_total(num_of_chunk)

    # Send file name
    clientSocket.sendto(filename.encode('utf-8'), (const.SERVER_IP, const.SERVER_PORT))
    msg = clientSocket.recv(2)

    receiver_port = int.from_bytes(msg, byteorder='little')

    for chunk in chunk_generator:
        counter += 1

        packet = None

        if counter==num_of_chunk:
            packet = packet_class.create_last_packet(chunk)
        else:
            packet = packet_class.create_packet(chunk)

        clientSocket.sendto(packet, (const.SERVER_IP, receiver_port))
        acknowledgement =  int.from_bytes(clientSocket.recv(1024), byteorder='little')
        progress_bar.printProgressBar(counter)
    
def main():
    file_list = []

    if (len(sys.argv) < 2):
        print ("You must specify file name in argument")
        sys.exit()
    elif (len(sys.argv) < 7):
        for i in range(1, len(sys.argv)):
            file_list.append(sys.argv[i])
    else:
        print ("You cannot send more than 5 file")
        sys.exit()

    pool = multiprocessing.Pool(processes = 100)

    for filename in file_list:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(filename)
        new_sender_process = pool.apply_async(send_thread, (filename, const.SERVER_IP, clientSocket))
    
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
