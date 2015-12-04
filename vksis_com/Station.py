import serial 
from bit_stuffing import*
from Hamming import*
from multiprocessing import pool

class Packet:
    '''
    FI - frame info
    DA - destination Address
    SA - source address
    M - monitor bit
    A - address recognized bit    
    C - frame-copied bit
    '''
    def __init__(self,frame = None):
        self.bitStuffing = bit_stuffing()
        self.hamming = Hamming()
        self.frame = frame
        if not frame:
            self.FI = bitarray(8)
            self.DA = None
            self.SA= None
        else:
            self.extractFrameInfo()

    @property
    def monitor(self):
        return self.FI[2]

    @monitor.setter
    def frameInfoMonitor(self,value):
        self.FI[2] = value       

    @property
    def addrRecognized(self):
        return self.FI[1]

    @addrRecognized.setter
    def addrRecognized(self,value):
        self.FI[1] = value
    
    @property
    def frameCopied(self):
        return self.FI[0]

    @frameCopied.setter
    def frameCopied(self,value):
        self.FI[0] = value

    def pack(self,payload):
        #bit stuffing
        payload,pBitStuffed = self.bitStuffing.encode(payload) 
        #hamming encode
        payload  = self.hamming.encode(payload)
        # packet = FD + FI + DA + SA + payload + FD
        FD = self.bitStuffing.byteFD
        packet = FD +   stufHamPayload + FD
        self.frame =  packet + self.FI.tobytes() + self.DA + self.SA + payload + FD
        return self.frame

    def extractFrameInfo(self):
        self.FI = bitarray()
        self.FI.frombytes(self.frame[1])
        self.DA = self.frame[2]
        self.SA = self.frame[3]


    def unpack(self):
        self.extractFrameInfo()
        payload = frame[4 : len(self.frame)-1]
        #hemming decode
        payload = self.hamming.decode(bytes(payload))
        #bit stuffing decode
        payload,pBitStuffed = self.bitStuffing.decode(payload)
        return payload


class Station:
   
    def __init__(self):
        #ports to communicate with circle
        self.prevPortName = 'COM2'
        self.nextPortName = 'COM3'
        self.nextPort = None
        self.prevPort = None
        self.isMonitor = False
        self.address = None

    def run(self,address,isMonitor):
        #if combobox is selected as monitor-> true else folse
        self.address = address
        self.isMonitor = isMonitor
        #open ports
        '''
        The port is immediately opened on object creation, when a port is given.
        It is not opened when port is None and a successive call to open() will be needed.
        '''
        self.prevPort = serial.Serial(self.prevPortName)
        self.nextPort = serial.Serial(self.nextPortName)

   
    def send(self,data,destAddr):
        pack = Packet()
        #set frame monitor bit
        pack.monitor = self.isMonitor
        #dest address
        pack.SA = self.address
        pack.DA = destAddr
        pack.pack(data)
        self.nextPort.write(pack.frame)

    def transit(self):
        while True:
            #get packet (frame)
            pack = self.receive()
            #if cur station address == destination address
            if self.address == pack.DA:
                #get packet data
                payload = self.acceptPacket(pack)
                if payload is not None:
                    return payload
            else:
                self.redirectPacket(pack)


    def acceptPacket(self,pack):
        #check if the packet is from this station 
        #and receiver get data from it
        if not (pack.addrRecognized and pack.frameCopied): 
            #swap DA and SA and send pack to sender
            pack.DA , pack.SA = pack.SA , pack.DA 
            #if monitor station, set M bit
            pack.monitor = self.isMonitor
            #set address_recognized and frame_copied bits
            pack.addrRecognized = True
            pack.frameCopied = True
            self.nextPort.write(pack.frame)
            return pack.unpack()
        #else destroy packet
        else: return None

    def redirectPacket(self,pack):
        #if not monitor bit and station is monitor, set it
        if self.isMonitor and (not pack.monitor):
            pack.monitor = True
            self.nextPort.write(pack)
            #else drop packet
        else:
            #if not monitor -> redirect always 
            self.nextPort.write(pack)

    def receive(self):
        #read until the FD
        FD = self.bitStuffing.byteFD
        frame = []
        #finding packet beginning
        byte = None
        while byte != FD:
             byte = self.prevPort.read(1)
        #put first FD
        frame.append(byte[0])
        byte = None
        while byte != FD:
            byte = self.prevPort.read(1)
            frame.append(byte[0])
        #put last FD
        frame.append(byte[0])
        packet = Packet(bytes(frame))
        return packet
         
         

