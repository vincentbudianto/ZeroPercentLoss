SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

DATA    = int('0x0', 16)
ACK     = int('0x1', 16)
FIN     = int('0x2', 16)
FINACK  = int('0x3', 16)

TYPE_LENGTH = 4
ID_LENGTH   = 4
SEQ_NUM_LENGTH = 16
LEN_LENGTH = 16
CHECKSUM_LENGTH = 16
TIMEOUT = 2

THIRTYTWO_KB = 32768;

INDEX_DATA = 0
INDEX_TYPEVAR = 1
INDEX_IDVAR = 2
INDEX_SEQNUM = 3
INDEX_LENGTH = 4