from bit_stuffing import*
from Hamming import*
from multiprocessing import pool

class Station:
    
    def __init__(self):
        self.bitStuffing = bit_stuffing()
        self.hamming = Hamming()
        #ports to communicate with circle
        self.next_port = None
        self.prev_port = None


    def send(self,port,constBytes):
        #bit stuffing
        stuffedPayload,pBitStuffed = self.bitStuffing.encode(constBytes) 
        #hamming encode
        stufHamPayload  = self.hamming.encode(stuffedPayload)
        payloadLen = len(stufHamPayload)
        # packet = FD + payload + FD
        packet = self.bitStuffing.byteFD + stufHamPayload + self.bitStuffing.byteFD
        port.write(packet)


    def receive(self,port):
        #read until the FD
        FD = self.bitStuffing.byteFD
        payload = []
        #finding packet beginning
        while True:
             byte = port.read(1)
             if byte == FD:
                 break
        #read data
        payloadLen = 0
        byte = 0
        while True:
            byte = port.read(1)
            if byte == FD: 
                break
            payload.append(byte[0])
        #hemming decode
        hamPayload = self.hamming.decode(bytes(payload))
        #bit stuffing decode
        hamStufpayload,pBitStuffed = self.bitStuffing.decode(hamPayload)
        return hamStufpayload 