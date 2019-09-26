from file import *
from packet import Packet
import const
import multiprocessing
import os
import socket
import struct
import time

def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def receive_thread(file_name, client_address, thread):
    receiver_port = thread.get()
    print('getting port: {}, client: {}'.format(receiver_port, client_address))
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_socket.bind((get_my_ip(), receiver_port))

    # send our port
    port_message = receiver_port.to_bytes(2, byteorder='little')
    print('sending port, {}'.format(client_address))
    receiver_socket.sendto(port_message, client_address)

    # opening to be written file
    destination_path = get_destination_directory()
    full_path = destination_path+'/'+file_name

    if (os.path.exists(full_path)):
        os.remove(full_path)

    destination_file = open(full_path, 'ab')

    counter = 0
    # receiving data
    delayed_checksum = None
    latest_seq_num = -1
    while True:
        counter += 1
        packet = receiver_socket.recv(35000)

        valid, packet_data = Packet.read_packet_from_bytes_array(bytearray(packet))

        # verify packet
        if not(valid):
            continue

        seq_num = packet_data[const.INDEX_SEQNUM]
        if (seq_num != (latest_seq_num + 1)):
            continue

        if (delayed_checksum):
            print(str(delayed_checksum)+'    '+str(packet_data[const.INDEX_CHECKSUM]))
            delayed_checksum = None

        # send ack
        file_chuck = packet_data[const.INDEX_DATA]
        # if counter%150==0:
        #     delayed_checksum = packet_data[const.INDEX_CHECKSUM]
        #     print('delayed')
        #     time.sleep(2)
        #     continue

        destination_file.write(file_chuck)
        latest_seq_num = seq_num

        if packet_data[const.INDEX_TYPEVAR] == FIN:
            receiver_socket.sendto(const.FINACK.to_bytes(1, byteorder='little'), client_address)
            destination_file.close()
            break
        else:

            receiver_socket.sendto(const.ACK.to_bytes(1, byteorder='little'), client_address)

def main():
    SERVER_PORT = int(input("Enter server port: "))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((get_my_ip(), SERVER_PORT))
    print("UDP server up and listening")
    print("Server IP: {} | PORT: {}".format(get_my_ip(), SERVER_PORT))

    pool = multiprocessing.Pool(processes = 100)

    pool_manager = multiprocessing.Manager()
    port_queue = pool_manager.Queue()

    portList = range(5001, 6000)

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
