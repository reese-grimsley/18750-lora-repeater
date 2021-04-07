
MAX_PACKET_SIZE_BYTES = 64

class TXMessage():

    def  __init__(self, frame_count: int, client_addr, payload):
        '''
        A message to send with a few minor features in the header, namely a frame-count and a sender address in addition to the payload. This class encodes that into a stream of bytes for the PHY layer

        frame_count: int, 2 bytes long
        client_addr: int, 1 byte long (it's a small system...)
        payload: str or bytes, contains the message to send
        '''

        assert len(payload) < MAX_PACKET_SIZE_BYTES, f'Message is too large to send at {len(payload)} bytes'
        assert frame_count > 0, 'Frame count is negative'
        assert frame_count & 0xffff == frame_count, 'Frame count is too high; it should be within 2 bytes'

        self.frame_count = frame_count
        self.client_addr = client_addr
        self.payload = payload
        if isinstance(payload, bytes):
            self.payload_bytes = payload
        elif isinstance(payload, str):
            #convert from string (utf-8 by default) into a byte array as ascii format
            self.payload_bytes = (bytes)(payload, 'utf-8')
            
        else:
            raise TypeError('payload should be a set of bytes or a string to send')

        # print(self.payload_bytes)
        self.bytes = int.to_bytes(self.frame_count, 2, byteorder='big', signed=False) + int.to_bytes(self.client_addr, 4, byteorder='big', signed=False) +  self.payload_bytes 

        ##bytes.hex(tx.get_bytes()) == hexlify(tx.bytes).decode('ascii')

    def get_bytes(self):
        return self.bytes

class RXMessage():
    '''
    A class to decode the received bytes in the same way that the TXMessage encodes them

    msg_str: the string of hex bytes received from the rak811v2 library

    '''
    def __init__(self, msg_str):
        self.msg_str = msg_str
        msg_bytes = bytes.fromhex(self.msg_str)

        self.frame_count  = int.from_bytes(msg_bytes[0:2], byteorder='big')
        self.client_addr = int.from_bytes(msg_bytes[2:6], byteorder='big')
        self.payload = msg_bytes[6:].decode('ascii')

    def get_payload(self):
        return self.payload

    def get_addr(self):
        return self.client_addr

    def get_frame_counter(self):
        return self.frame_count