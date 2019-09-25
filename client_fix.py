from packet import *
from file import File
from progressbar import *
import const
import file
import pickle
import socket
import time
import sys

progress_bar = ProgressBar()

def main():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.settimeout(5)

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

    for filename in file_list:
        path = '{}/' + filename
        file_path = filename.format(file.get_current_directory())
        file_obj = File(file_path)

        chunk_generator = file_obj.get_chunks_generator()
        num_of_chunk = file_obj.calculate_chunks_number()

        packet_class = Packet(1)

        dest_name = 'lala.' + filename[-3:]
        new = open(dest_name, 'ab')

        counter = 0
        progress_bar.set_total(num_of_chunk)

        for chunk in chunk_generator:
            packet = packet_class.create_packet(chunk)

            try:
                clientSocket.sendto(packet, (const.SERVER_IP, const.SERVER_PORT))
                data, address = clientSocket.recvfrom(1024)
                new_chunk = packet_class.read_packet_from_bytes_array(packet)

                counter += 1
                progress_bar.printProgressBar(counter)

                new.write(new_chunk)

            except(TimeoutError):
                print('No, response. Try again')

            # send file to server
            # receive acknowledgement from server

        print(counter)


if __name__ == '__main__':
    main()
