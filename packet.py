from const import *

class Packet:
    def __init__(self, id):
        self.type = None
        self.id = id
        self.seq_num = 0
        self.length = 0
        self.checksum = None
        self.data = None

    def create_packet_with_type(self, file_chunk, type):
        self.type = type
        self.length = len(file_chunk)
        self.data = file_chunk
        self.seq_num += 1

    def create_packet(self, file_chunk):
        self.create_packet_with_type(file_chunk, DATA)

    def create_last_packet(self, file_chunk):
        self.create_packet_with_type(file_chunk, FIN)

    def to_bits(self):
        bits = self.id | self.type << ID_LENGTH
        bits |= self.seq_num << (TYPE_LENGTH + ID_LENGTH)
        bits |= self.length << (TYPE_LENGTH + ID_LENGTH + SEQ_NUM_LENGTH)
        bits |= DATA << (TYPE_LENGTH + ID_LENGTH + SEQ_NUM_LENGTH + LEN_LENGTH)
        return bits

    def checksum(self):
        checksum = 0
        appended = self.to_bits()
        bits_taker = (2<<16)-1
