from file import File
from packet import *
from progressbar import *
import const
import file
import multiprocessing
import pickle
import socket
import time
import sys
import hashlib

_TERMINATE = False
progress_bar = ProgressBar()

def send_thread(filename, server_address):
    stop = False

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.settimeout(1)

    counter = 0
    retry_counter = 0

    path = '{}/' + filename
    file_path = path.format(file.get_source_directory())
    file_obj = File(file_path)

    chunk_generator = file_obj.get_chunks_generator()
    num_of_chunk = file_obj.calculate_chunks_number()

    packet_class = Packet(counter)
    progress_bar.set_total(num_of_chunk)

    # Send file name
    clientSocket.sendto(filename.encode('utf-8').strip(), server_address)
    server_port = clientSocket.recv(2)

    receiver_port = int.from_bytes(server_port, byteorder='little')
    for chunk in chunk_generator:
        if (_TERMINATE):
            thread.terminate()

        counter += 1

        packet = None
        success = False

        if counter==num_of_chunk:
            packet = packet_class.create_last_packet(chunk)
        else:
            packet = packet_class.create_packet(chunk)

        while not(success):
            if (retry_counter > 4):
                print("\n\nServer not responding")
                stop = True
                break
            try:
                clientSocket.sendto(packet, (server_address[0], receiver_port))
                acknowledgement =  int.from_bytes(clientSocket.recv(1024), byteorder='little')
                success = True
                retry_counter = 0
            except:
                print('\n\n<<<     RETRYING    >>>', end='\r')
                retry_counter += 1

        if(stop):
            thread.terminate()
            break

        progress_bar.printProgressBar(counter, filename)

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

    # SERVER_IP = input("Server IP Address: ")
    # SERVER_PORT = int(input("Server Port: "))

    pool = multiprocessing.Pool(processes = 100)

    for filename in file_list:
        new_sender_process = pool.apply_async(send_thread, (filename, (SERVER_IP, SERVER_PORT)))

    _TERMINATE = True
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
