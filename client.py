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

progress_bar = ProgressBar()
total_chunk = 0

def send_thread(filename, server_address):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # clientSocket.settimeout(5)

    counter = 0

    path = '{}/' + filename
    file_path = path.format(file.get_source_directory())
    file_obj = File(file_path)

    chunk_generator = file_obj.get_chunks_generator()
    num_of_chunk = file_obj.calculate_chunks_number()

    packet_class = Packet(counter)
    progress_bar.set_total(num_of_chunk)

    # Send file name
    print(filename)
    print(type(filename))
    clientSocket.sendto(filename.encode('utf-8').strip(), server_address)
    server_port = clientSocket.recv(2)

    receiver_port = int.from_bytes(server_port, byteorder='little')

    for chunk in chunk_generator:
        counter += 1

        packet = None

        if counter==num_of_chunk:
            packet = packet_class.create_last_packet(chunk)
        else:
            packet = packet_class.create_packet(chunk)

        clientSocket.sendto(packet, (server_address[0], receiver_port))
        acknowledgement =  int.from_bytes(clientSocket.recv(1024), byteorder='little')

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
    SERVER_IP = '192.168.43.136'
    # SERVER_PORT = int(input("Server Port: "))
    SERVER_PORT = 5000

    pool = multiprocessing.Pool(processes = 100)

    for filename in file_list:
        new_sender_process = pool.apply_async(send_thread, (filename, (SERVER_IP, SERVER_PORT)))

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
