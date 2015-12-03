import sys  #for COM name
import serial 
from bitarray import*
import threading
from bit_stuffing import bit_stuffing
from Station import Station
from tkinter import*
from tkinter.ttk import*    #ovveride tkinter widgets
from Hamming import Hamming

class Application(Frame):
   

    def __init__(self,master = None):
        super().__init__(master)
        self.pack()
        self.station = Station()
        #binds station name and com ports for it
        self.stations =  {'monitor':('COM2','COM3'),
                          'station_1':('COM4','COM5'),
                          'station_2':('COM6','COM7')
                         }
        self.__createWidgets()


    def __del__(self):
        self.destroy()
        self.quit()


    def __createWidgets(self):
        self.grid()
        #statins combobox
        self.stationsCombo = Combobox(self,values= list(self.stations.keys()))
        #set monitor at first
        self.stationsCombo.set('monitor')
        self.stationsCombo.grid(column=0,row=0,sticky='nwse')
        #stations label
        self.stationsLabel = Label(self,text='station',font='Arial 8')
        self.stationsLabel.grid(column=2,row=0,sticky='w')
        #open port button
        self.openPortsBut = Button(self,text='open ports',command=self.openPortsEvent)
        self.openPortsBut.grid(column=0,row=1,sticky='nwse')
        #send button
        self.sendBut = Button(self,text="send",command=self.sendEvent)
        self.sendBut.grid(column=0,row=2,sticky='nwse')
        #address combo 
        self.addressCombo = Combobox(self,values=list(self.stations.keys()))
        self.addressCombo.set('monitor')
        self.addressCombo.grid(column=0,row=3,sticky='nwse')
        #address label
        self.addressLabel = Label(self,text='addressed to',font='Arial 8')
        self.addressLabel.grid(column=2,row=3,sticky='w')
        #edit text
        self.textbox = Text(self,height=12,width=64,font='Arial 8',wrap=WORD)
        self.textbox.focus_set()
        self.textbox.grid(column=0,row=4,columnspan=5)
        

    def openPortsEvent(self):
        pass

    def sendEvent(self):
        msg = self.textbox.get('1.0',END)
        self.protocol.send(msg.encode('utf-8'))
        

    def showPortData(self):
        '''
        while True:
            msg = self.protocol.receive().decode('utf-8')
            #show
            self.textbox.delete('1.0',END) 
            self.textbox.insert('1.0',msg)
        '''
    

    def parallelShowPortData(self):
        #readThread = threading.Thread(target=self.showPortData)
        #readThread.start()
        pass


def openSerialPort(name):

    #comPortsList = serial.tools.list_ports.comports()
    #portList = list(serial.tools.list_ports.comports())
    #if any(name == port for port  in serial.tools.list_ports.comports()) != True:
    #    raise serial.SerialException("there is no such port name")
    '''
    The port is immediately opened on object creation, when a port is given.
    It is not opened when port is None and a successive call to open() will be needed.
    '''
    port = serial.Serial(name)
    if port.isOpen() != True:
        raise serial.SerialException("can't open the port")
    return port
     
         
if __name__ == "__main__":
    '''
    if(len(sys.argv) < 2):
        sys.exit(1)
    try:
        port = openSerialPort(sys.argv[1])
    except serial.SerialException as e:
        print(e.args[0])
        sys.exit(1)
    '''
    root = Tk()
    app = Application(master=root)
    app.parallelShowPortData()
    app.mainloop()


