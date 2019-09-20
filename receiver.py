from progressbar import *
import select
import socket
import sys

#cek ip di cmd 'ipconfig' liat yg IPv4 Address
#port bebas asal sender sama receiver punya port yg sama

ip = '192.168.43.150' # Oksi
port = 5005
buffer = 1024
address = (ip, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
sock.bind(address)

f = open('file.pdf','wb')

data, address = sock.recvfrom(buffer)

try:
    while(data):
        f.write(data)
        sock.settimeout(2)
        data,address = sock.recvfrom(buffer)
except socket.timeout:
    f.close()
    socket.close()
    print('File Downloaded')
