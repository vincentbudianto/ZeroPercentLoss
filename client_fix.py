import file
from file import File
import socket
import const
import pickle
import time

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((socket.gethostname(), const.SERVER_PORT))

test_file_path = '{}/test.zip'.format(file.get_current_directory())
test_file_obj = File(test_file_path)

chunkGenerator = test_file_obj.get_chunks_generator()
num_of_chunk = test_file_obj.calculate_chunks_number()

for chunks in chunkGenerator:
    # a+=1
    # print(type(chunks))
    print(len(chunks))
print(num_of_chunk)
# while True:
#     time1 = time.time()

#     for i in range(10000):
#         msg = {"msg" : str(i)}

#         tobesend = pickle.dumps(msg)

#         s.send(tobesend)

#         msg, sender = s.recvfrom(32)
#         print(msg.decode("utf-8"))

#     time2 = time.time()
#     print(time2-time1)
#     a = input()

