from progressbar import *
import socket
import sys

DATA = 0x0
ACK = 0x1
FIN = 0x2
FINACK = 0x3

host = '192.168.43.150' # Oksi
port = 5005
buffer = 1024
address = (host, port)
files = []

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP

inputFile = True

print('UDP target IP:', host)
print('UDP target port:', port)

while (inputFile and (len(files) < 5)):
    file_name = input('Masukan path dari file ke-%d: ' % (len(files) + 1))

    if (file_name == 'x'):
        inputFile = False
    else:
        files.append(file_name)

sock.sendto(file_name,address)

for i in files:
    f = open(i, 'rb')
    data = f.read(buffer)

    while (data):
        if (sock.sendto(data, address)):
            print('Sending ...')
            data = f.read(buffer)

    sock.close()
    f.close()

print('Files:')
for i in files:
    print(i)
#    sock.sendto(i.encode(), (host, port))

checksum = list(range(0, 51))
l = len(checksum)

printProgressBar(0, l)
for i, item in enumerate(checksum):
    time.sleep(0.1)
    printProgressBar(i + 1, l)