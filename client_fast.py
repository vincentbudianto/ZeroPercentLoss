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
import logging
logging.basicConfig(level=logging.INFO)


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

    next_packet = packet_class.create_packet(next(chunk_generator))
    cur_packet = None
    for chunk in chunk_generator:
        counter += 1

        success = False

        cur_packet = next_packet

        while not(success):
            if (retry_counter > 9):
                print("\n\nServer not responding")
                stop = True
                break
            try:
                clientSocket.sendto(cur_packet, (server_address[0], receiver_port))
                if (counter == num_of_chunk-1 and retry_counter==0):
                    next_packet = packet_class.create_last_packet(chunk)
                elif (counter < num_of_chunk-1 and retry_counter==0):
                    next_packet = packet_class.create_packet(chunk)

                acknowledgement =  int.from_bytes(clientSocket.recv(1024), byteorder='little')
                success = True
                retry_counter = 0

            except Exception as e:
                print('\n\n<<<     RETRYING    >>>', end='\r')
                retry_counter += 1

        if (stop):
            break

        progress_percent = ceil(counter/num_of_chunk*100.0)
        with lock:
            progress.value = progress_percent

    clientSocket.sendto(next_packet, (server_address[0], receiver_port))
    acknowledgement =  int.from_bytes(clientSocket.recv(1024), byteorder='little')



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

    all_start_time = time.time()
    while processes:
        processes = [process for process in processes if process.is_alive()]
        for idx, process in enumerate(processes):
            progress_bar_class.print_progress_bar(progress_poll[idx].value, file_list[idx])
        sys.stdout.write(u"\u001b[2J")
        time.sleep(0.1)

    print('Transfer complete! {}s elapsed'.format(time.time()-all_start_time))
if __name__ == '__main__':
    main()
