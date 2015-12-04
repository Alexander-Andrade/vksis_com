import sys  #for COM name
from bitarray import*
import threading
from bit_stuffing import bit_stuffing
from Station import*
from tkinter import*
from tkinter.ttk import*    #ovveride tkinter widgets
from Hamming import Hamming

class Application(Frame):
   

    def __init__(self,master = None):
        super().__init__(master)
        self.pack()
        self.station = Station()
        #binds station name and com ports for it
        self.stations =  [1, 2, 3]
        self.portsDict = {self.stations[0] : ('COM3','COM2'),
                          self.stations[1] : ('COM5','COM4'),
                          self.stations[2] : ('COM7','COM6')} 
        self.__createWidgets()
        self.flPortsOpen = False


    def __del__(self):
        self.destroy()
        self.quit()


    def __createWidgets(self):
        self.grid()
        #statins combobox
        self.stationsCombo = Combobox(self,values = self.stations)
        #set monitor at first
        self.stationsCombo.set(self.stations[0])
        self.stationsCombo.grid(column=0,row=0,sticky='nwse')
        #stations label
        self.stationsLabel = Label(self,text='station',font='Arial 8')
        self.stationsLabel.grid(column=2,row=0,sticky='w')
        #open port button
        self.openPortsBut = Button(self,text='open ports',command=self.openPortsEvent)
        self.openPortsBut.grid(column=0,row=1,sticky='nwse')
        #open port label
        self.openPortLabel = Label(self,text='closed',font='Arial 8')
        self.openPortLabel.grid(column=2,row=1,sticky='w')
        #send button
        self.sendBut = Button(self,text="send",command=self.sendEvent)
        self.sendBut.grid(column=0,row=2,sticky='nwse')
        #address combo 
        self.addressCombo = Combobox(self,values=self.stations)
        self.addressCombo.set(self.stations[0])
        self.addressCombo.grid(column=0,row=3,sticky='nwse')
        #address label
        self.addressLabel = Label(self,text='addressed to',font='Arial 8')
        self.addressLabel.grid(column=2,row=3,sticky='w')
        #edit text
        self.textbox = Text(self,height=12,width=64,font='Arial 8',wrap=WORD)
        self.textbox.focus_set()
        self.textbox.grid(column=0,row=4,columnspan=5)
        #error Label
        self.errorLabel = Label(self,text='no errors',font='Arial 8')
        self.errorLabel.grid(column=0,row=5,sticky='w')
        

    def openPortsEvent(self):
        stationAddr =  self.stationsCombo.get()
        isMonitor = self.stations[0] == int(stationAddr)
        self.station.run(self.stationsCombo.get(),isMonitor,self.portsDict[int(stationAddr)])
        self.openPortLabel['text'] = 'opened: ' + stationAddr
        self.flPortsOpen = True
        self.parallelShowPortData()

    def sendEvent(self):
        try:
            if not self.flPortsOpen:
                raise serial.SerialException('ports are close')
            msg = self.textbox.get('1.0',END)
            self.station.send(int(self.addressCombo.get()),msg.encode('utf-8'))
            #all is clear
            self.errorLabel['text'] = ''
        except (serial.SerialException, AddrError) as e:
            self.errorLabel['text'] = e
        

    def showPortData(self):
        while True:
            msg = self.station.transit().decode('utf-8')
            #show
            self.textbox.delete('1.0',END) 
            self.textbox.insert('1.0',msg)
        
    

    def parallelShowPortData(self):
        readThread = threading.Thread(target=self.showPortData)
        readThread.start()
        
     
if __name__ == "__main__":
    
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    
    #st = Station()
    #st.run(1,True,('COM2','COM3'))

