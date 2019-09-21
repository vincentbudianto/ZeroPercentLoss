from progressbar import *
import select
import socket
import sys

DATA = 0x0
ACK = 0x1
FIN = 0x2
FINACK = 0x3

#cek ip di cmd 'ipconfig' liat yg IPv4 Address
#port bebas asal sender sama receiver punya port yg sama

ip = '192.168.43.150' # Oksi
port = int(input("Port: "))
#port = 5005
buffer = 1024
address = (ip, port)

ack = False

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
serverSocket.bind(address)

try:
    f = open('file.pdf','wb')
    data, address = serverSocket.recvfrom(12)

    while(data):
        f.write(data)
        serverSocket.settimeout(2)
        data,address = serverSocket.recvfrom(buffer)
except socket.timeout:
    f.close()
    serverSocket.close()
    print('File Downloaded')

checksum = list(range(0, 51))
l = len(checksum)

printProgressBar(0, l)
for i, item in enumerate(checksum):
    time.sleep(0.1)
    printProgressBar(i + 1, l)