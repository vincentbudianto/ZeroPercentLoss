import const
import multiprocessing
import pickle
import socket
import struct
import time

portList = range(5001, 6000)

def send_data(port, thread, data):
    sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sendSocket.bind((const.SERVER_IP, port))
    # sendSocket.settimeout(5)

    try:
        sendSocket.sendto(data, (const. SERVER_IP, port+1))
        # print('port ==> ', port)
        # print()
        # print('Received message : "{}"'.format(data))
        # print()
        # print()
    finally:
        thread.put(port)

def receive(message, address, thread):
    p = thread.get()
    data = pickle.loads(message)
    send_data(p, thread, data)

def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((const.SERVER_IP, const.SERVER_PORT))
    print("UDP server up and listening")
    print("Server IP: {} | PORT: {}".format(const.SERVER_IP, const.SERVER_PORT))

    pool = multiprocessing.Pool(processes = 100)

    poolManager = multiprocessing.Manager()
    thread = poolManager.Queue()

    for port in portList:
        thread.put(port)

    while True:
        message, address = serverSocket.recvfrom(999999)
        # clientMsg = "Message from Client:{}".format(message)
        # clientIP  = "Client IP Address:{}".format(address)
        # print(clientMsg)
        # print(clientIP)

        data = pool.apply_async(receive, (message, address, thread, serverSocket))
        serverSocket.sendto(bytes("Data acknowleged!", "utf-8"), address)

if __name__ == '__main__':
    main()
