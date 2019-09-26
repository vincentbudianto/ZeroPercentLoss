from file import File
from packet import *
from progressbar import *
import const
import file
import multiprocessing
from multiprocessing import Process, Value, Lock
import pickle
import socket
import time
import sys
import hashlib
from math import ceil


def send_thread(filename, server_address, progress, lock):
    stop = False

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.settimeout(1)

    counter = 0
    retry_counter = 0

    path = '{}/' + filename
    file_path = path.format(file.get_source_directory())

    try:
        file_obj = File(file_path)
    except FileNotFoundError:
        print('\n\n<<<     FILE NOT FOUND     >>>\n')

    chunk_generator = file_obj.get_chunks_generator()
    num_of_chunk = file_obj.calculate_chunks_number()

    packet_class = Packet(counter)

    # Send file name
    clientSocket.sendto(filename.encode('utf-8').strip(), server_address)
    server_port = clientSocket.recv(2)

    receiver_port = int.from_bytes(server_port, byteorder='little')

    for chunk in chunk_generator:
        counter += 1

        success = False

        if (counter == num_of_chunk):
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

        if (stop):
            break

        progress_percent = ceil(counter/num_of_chunk*100.0)
        with lock:
            progress.value = progress_percent

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

    SERVER_IP = input("Server IP Address: ")
    SERVER_PORT = int(input("Server Port: "))
    server_addr = (SERVER_IP, SERVER_PORT)

    jumlah_file = len(sys.argv)-1

    progress_poll = [Value('i', 1) for x in range(jumlah_file)]
    lock = Lock()

    processes = [Process(target=send_thread, args=(file_list[i], (SERVER_IP, SERVER_PORT), progress_poll[i], lock)) for i in range(jumlah_file)]

    for process in processes : process.start()

    max_length = len(max(file_list, key=len))
    progress_bar_class = ProgressBar(max_length)

    while True:
        for idx, progress in enumerate(progress_poll):
            progress_bar_class.print_progress_bar(progress.value, file_list[idx])
        sys.stdout.write(u"\u001b[2J")
        time.sleep(0.01)

    for process in processes : process.join()
if __name__ == '__main__':
    main()
