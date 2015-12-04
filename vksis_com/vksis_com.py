import sys  #for COM name
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
        self.stations =  ['monitor', 'station_1', 'station_2']
        self.__createWidgets()


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
        

    def openPortsEvent(self):
        stationAddr =  self.stationsCombo.get()
        isMonitor = self.stations[0] == stationAddr
        self.station.run(self.stationsCombo.get(),isMonitor)

    def sendEvent(self):
        msg = self.textbox.get('1.0',END)
        self.station.send(msg.encode('utf-8'))
        

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
        
    
class MyClass:
    
    def __init__(self):
        self.i = 5

    @property
    def I(self):
        return self.i
    
    @I.setter
    def I(self,val):
        self.i = val + 5
     
if __name__ == "__main__":
    root = Tk()
    app = Application(master=root)
    app.parallelShowPortData()
    app.mainloop()
    

