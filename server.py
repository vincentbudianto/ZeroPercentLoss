import struct
import socket
import const
import pickle
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), const.SERVER_PORT))
s.listen(5)

while True:
    clientSocket, address = s.accept()

    while True:
        msg, source = clientSocket.recvfrom(32)

        data = pickle.loads(msg)

        print('Received message : "{}"'.format(data))

        clientSocket.send(bytes("Data acknowleged!", "utf-8"))