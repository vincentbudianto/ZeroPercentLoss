from file import *
from packet import Packet
import const
import multiprocessing
import os
import socket
import struct
import time

portList = range(5001, 6000)

def receive_thread(file_name, client_address, thread):
    receiver_port = thread.get()
    print('getting port: {}, client: {}'.format(receiver_port, client_address))
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_socket.bind((const.SERVER_IP, receiver_port))
    receiver_socket.settimeout(5)

    try:
        # send our port
        port_message = receiver_port.to_bytes(2, byteorder='little')
        receiver_socket.sendto(port_message, client_address)

        # opening to be written file
        destination_path = get_destination_directory()
        full_path = destination_path+'/'+file_name
        destination_file = open(full_path, 'ab')

        # receiving data
        while True:
            packet = receiver_socket.recv(35000)
            a = bytes(packet)
            valid, packet_data = Packet.read_packet_from_bytes_array(bytearray(packet))

            # verify packet
            if not valid:
                continue

            # send ack
            file_chuck = packet_data[const.INDEX_DATA]

            destination_file.write(file_chuck)

            if packet_data[const.INDEX_TYPEVAR] == FIN:
                receiver_socket.sendto(const.FINACK.to_bytes(1, byteorder='little'), client_address)
                destination_file.close()
                break
            else:
                receiver_socket.sendto(const.ACK.to_bytes(1, byteorder='little'), client_address)
    except(TimeoutError):
        print('Timeout error detected. Please try again.')

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((const.SERVER_IP, const.SERVER_PORT))
    print("UDP server up and listening")
    print("Server IP: {} | PORT: {}".format(const.SERVER_IP, const.SERVER_PORT))

    pool = multiprocessing.Pool(processes = 100)

    pool_manager = multiprocessing.Manager()
    port_queue = pool_manager.Queue()

    for port in portList:
        port_queue.put(port)

    while True:
        file_name, client_address = server_socket.recvfrom(const.THIRTYTWO_KB)
        file_name = file_name.decode('utf-8')
        print('Receiving file: %s\n'% file_name)

        # create new receiver process
        new_receiver_process = pool.apply_async(receive_thread, (file_name, client_address, port_queue))

if __name__ == '__main__':
    main()
