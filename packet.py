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

        self.byte_array = self.to_byte_array()
        self.checksum = self.create_checksum(self.byte_array)

        self.byte_array.insert(5, self.checksum[0])
        self.byte_array.insert(5, self.checksum[1])

        self.seq_num += 1

    def create_packet(self, file_chunk):
        self.create_packet_with_type(file_chunk, DATA)
        return self.byte_array

    def create_last_packet(self, file_chunk):
        self.create_packet_with_type(file_chunk, FIN)
        return self.byte_array

    def to_byte_array(self):
        bits = self.type | self.id << ID_LENGTH
        bits |= self.seq_num << (TYPE_LENGTH + ID_LENGTH)
        bits |= self.length << (TYPE_LENGTH + ID_LENGTH + SEQ_NUM_LENGTH)
        baitarray = bytearray(bits.to_bytes(5, byteorder="little"))
        baitarray += self.data
        return baitarray

    @staticmethod
    def create_checksum(data):
        appended = False
        if len(data)%2==1:
            data.append(0)
            appended=True

        checksum = 0
        idx = 0
        while idx < len(data):
            current_num = data[idx] | data[idx+1]<<8
            checksum = checksum ^ current_num
            idx += 2

        if appended:
            del data[-1]

        return (checksum).to_bytes(2, byteorder="little")

    @staticmethod
    def read_packet_from_bytes_array(bytes_array):
        copy_byte = bytes_array
        data = bytes(bytes_array[7:])
        checksum = bytes_array[6] | (bytes_array[5] << 8)

        typeid = bytes_array[0]
        typevar = ((1<<4)-1) & typeid
        idvar = typeid >> 4
        seq_num = (bytes_array[2] << 8)| bytes_array[1]
        length = (bytes_array[4] << 8) | bytes_array[3]

        # del checksum
        del copy_byte[5]
        del copy_byte[5]

        calculated_checksum = Packet.create_checksum(copy_byte)

        if (checksum == int.from_bytes(calculated_checksum, byteorder="little")):
            return (True, [data, typevar, idvar, seq_num, length, checksum])

        return (False, None)