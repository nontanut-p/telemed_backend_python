from termios import PARMRK
import tkinter as tk
from tkinter import Message, ttk
import serial
import serial.tools.list_ports
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import keyboard
import time
import datetime

class ParentClass:
    time_start = ''
    macd_thredshold = 1.25
    short_MV = 30
    portName = '/dev/ttyACM0'
    connection_status = False
    baudrate = 57600
    baudrates = [9600,
                 14400, 19200, 38400, 57600, 115200, 128000, 256000]
    smovingAverage_List = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    lmovingAverage_List = [50, 70, 90, 110, 130, 150, 170, 200, 230, 250, 300]
    thresholds = [1.0, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35,
                  1.40, 1.45, 1.50, 1.60, 1.70, 1.80, 1.90, 2.0]
    st_dt = [0,50, 100, 150, 200, 250, 300]
    short_ma = 30
    long_ma = 150
    threshold = 1.25
    start_dt = 200
    dt_interval = 50
    string_data = ''
    frontData = []
    backData = []
    shortback = []
    longback = []
    shortfront = []
    longfront = []
    mstfront = []
    mstback = []
    interval_temp = 0
    detectStatus = 1  
    start = False

    def __init__(self, root, title):
        self.root = root
        root.title(title)
        root.geometry("890x580")
        root.configure(bg='light steel blue')
        self.fig = Figure()
        
        self.ax = self.fig.add_subplot(111)
        self.fig.patch.set_facecolor('lightsteelblue')
        self.ax.set_title('LATEX Mechanical Stability Time Detection')
        self.ax.set_xlabel('TIME (s)')
        self.ax.set_ylabel('Distance (mm)')
        #self.ax.set_facecolor('blue')
        #self.ax.set_ylim(0, 60)
        #self.lines = self.ax.plot([], [])[0]
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().place(x=1, y=20, width=750, height=500)
        self.canvas.draw()

    def start_stop(self):
        if self.connection_status == False:
            tk.messagebox.showinfo(
                title='START/STOP ', message="Please try to Connect with device again")
        if self.connection_status == True:
            if self.start == True:
                self.start = False
                message_tk = 'STOP'
                self.l10 = tk.Label(self.root, bg='red', width=10,
                                    text='STOP').place(x=100, y=500)
                tk.messagebox.showinfo(title='START/STOP ', message=message_tk)
		        
            else:
                self.start = True
                self.l10 = tk.Label(self.root, bg='lime', width=10,
                                    text='RUNNING').place(x=100, y=500)
                tk.messagebox.showinfo(title='START/STOP ', message='START')

    def on_select(self, event=None):
        # get selection from event
        self.select_portName = event.widget.get()
        st = self.select_portName.find('/')
        ed = self.select_portName.find(' ')
        print("test",self.select_portName[st:ed])
        self.portName = self.select_portName[st:ed]
        print("change port to: ", self.portName)

    def select(self, event=None, *name):
        # get selection from event
        name = event.widget.get()

    def connect(self):
        self.time_start = datetime.datetime.now()
        print('self portName', self.portName, self.baudrate)
        self.ser = serial.Serial(self.portName, self.baudrate)
        self.connection_status = True
        # self.ser.reset_input_buffer()
        # self.ser.flushInput()
        # self.ser.flushOutput()
        time.sleep(1)
        self.ser.flush()
        self.ser.flush()
        self.ser.reset_input_buffer()
        message_tx = 'Connected to ' + \
            str(self.portName) + ' with baudrate ' + str(self.baudrate)
        tk.messagebox.showinfo(title='Connection ',
                               message=message_tx)
        print(self.ser.name)
        print('Connected to ', self.portName,
              ' with baudrate ', self.baudrate)

    def plotting(self):
        if self.start == True:
            if self.ser.in_waiting > 0:
                self.tmp = self.ser.readline().decode("Ascii")
                #self.string_data = self.string_data + self.tmp
		        #print('try to ploting')
                # print(dataSplit[1])
                print(self.backData, 'data')
                self.ax.clear()
                self.ax.set_title('LATEX Mechanical Stability Time Detection')
                self.ax.set_xlabel('TIME (s)')
                self.ax.set_ylabel('Distance (mm)')
                #self.clearplot()
                try:
                    data_input = float(self.tmp)
                    #string_data = self.tmp.split()
                    #print(float(string_data[1]))
                    self.frontData.append(data_input)  # Data ชุดหน้า
                    print(data_input)
                    #self.backData.append(
                    #    float(string_data[1]))  # Data ชุดหลัง
                    # self.lines.set_ydata(self.frontData)
                    # self.lines.set_xdata(self.frontData)
                    
                    if len(self.frontData) <= self.short_ma :
                        self.shortfront.append(sum(self.frontData)/len(self.frontData))
                        self.longfront.append(sum(self.frontData)/len(self.frontData))
                    if len(self.frontData) > self.short_ma and len(self.frontData) < self.long_ma :
                        self.shortfront.append(sum(self.frontData[-self.short_ma:])/self.short_ma)
                        self.longfront.append(sum(self.frontData)/len(self.frontData))
                    if len(self.frontData) >= self.long_ma :
                        self.shortfront.append(sum(self.frontData[-self.short_ma:])/self.short_ma)
                        self.longfront.append(sum(self.frontData[-self.long_ma:])/self.long_ma)
                        ## Detection interval ##
                        try:
                            macd_temp = self.shortfront[-1:][0] - self.longfront[-1:][0]
                            print("MACD",macd_temp)
                        except:
                            print('can not calculated ') 
                    if len(self.frontData) >= 1000:
                        self.threshold = 1.0 
                    if len(self.frontData) > self.start_dt and macd_temp > self.threshold and self.detectStatus == 1:
                        self.mstfront.append(len(self.frontData))
                        print('MST DETECTED AT : ', len(self.longfront))
                        self.interval_temp = 0
                        self.detectStatus = 0
                    if self.interval_temp < self.dt_interval and self.detectStatus == 0:
                        self.interval_temp = self.interval_temp + 1    
                        print('interval temp ++ ', self.interval_temp) 
                    if self.interval_temp == self.dt_interval :
                        self.detectStatus = 1
                    if len(self.mstfront) > 0 :
                        for i in range(len(self.mstfront)) :
                            self.ax.axvline(x = self.mstfront[i], color = 'b', label = 'axvline - full height')

                    '''
                    if data lenght < short  --> add moving average but its number of data
                    
                    if data lenght > short but < long --> add short moving average  
                    if data lenbght > short and > long --> add short, long moving average and start detection
                    '''
                    #PLOTING
                    
                    self.ax.plot(self.frontData, color='yellow')
                    self.ax.plot(self.shortfront, color='red')
                    self.ax.plot(self.longfront, color='green')
                    #self.ax.set_xlim(0, (len(self.frontData)+50))
                    self.canvas.draw()
                    x = self.time_start
                    x = x.strftime("%X")
                    print(x)
                    name = x + '.png'
                    self.fig.savefig(name ,dpi=200)

                except:
                    pass

        self.root.after(1, self.plotting)

    def on_select_bb(self, event=None):

        self.baudrate = event.widget.get()
        print(event.widget.get())
        print("change baudrate to : ", self.baudrate)

    def serial_ports(self):
        return serial.tools.list_ports.comports()

    def agreement_changed(self):
        tk.messagebox.showinfo(title='Result',
                               message=self.agreement.get())

    def clearplot(self):
        self.ax.clear()
        self.frontData.clear()
        self.backData.clear()
        self.shortfront.clear()
        self.longfront.clear()
        self.mstfront.clear()
        self.ax.set_title('LATEX Mechanical Stability Time Detection')
        self.ax.set_xlabel('TIME (s)')
        self.ax.set_ylabel('Distance (mm)')
        self.canvas.draw()

    def create_program(self, root):
        self.var1 = tk.IntVar()
        self.agreement = tk.StringVar()
        self.root = root
        self.l = tk.Label(self.root, bg='white', width=20,
                          text='Plot Selection').place(x=700, y=70)
        self.l2 = tk.Label(self.root, bg='white', width=20,
                           text='Parameter').place(x=700, y=130)
        self.l3 = tk.Label(self.root, bg='white', width=10,
                           text='Short_MA').place(x=690, y=160)
        self.cb_br = ttk.Combobox(
            self.root, values=self.smovingAverage_List,  width=10).place(x=770, y=160)
        self.cb_br = ttk.Combobox(
            self.root, values=self.lmovingAverage_List,  width=10).place(x=770, y=190)
        self.l4 = tk.Label(self.root, bg='white', width=10,
                           text='Long_MA').place(x=690, y=190)
        self.cb_br = ttk.Combobox(
            self.root, values=self.thresholds,  width=10).place(x=770, y=220)
        self.l5 = tk.Label(self.root, bg='white', width=10,
                           text='Threshold').place(x=690, y=220)

        self.l6 = tk.Label(self.root, bg='white', width=10,
                           text='Start DT').place(x=690, y=250)
        self.cb_br = ttk.Combobox(
            self.root, values=self.st_dt,  width=10).place(x=770, y=250)
        self.l7 = tk.Label(self.root, bg='white', width=10,
                           text='DT Interval').place(x=690, y=280)

        self.l9 = tk.Label(self.root, bg='white', width=20,
                           text='**DT : Detection').place(x=700, y=310)
        self.l10 = tk.Label(self.root, bg='white', width=20,
                            text='STATUS :').place(x=0, y=500)

        self.cb_br = ttk.Combobox(
            self.root, values=self.st_dt,  width=10).place(x=770, y=280)
        self.clear = tk.Button(
            root, text='CLEAR PLOT', command=lambda: self.clearplot()).place(x=470, y=525)
        self.start = tk.Button(
            root, text='START/STOP', command=lambda: self.start_stop()).place(x=240, y=525)
        self.stop = tk.Button(
            self.root, text='PLOT/REPLOT', command=lambda: self.plotting()).place(x=350, y=525)
        self.cb = ttk.Combobox(self.root, values=self.serial_ports())
        self.cb_br = ttk.Combobox(self.root, values=self.baudrates)
        self.cb.grid(row=1, column=1, ipadx="100")
        self.cb_br.grid(row=1, column=2, ipadx="50")
        self.cb.bind('<<ComboboxSelected>>', self.on_select)
        self.cb_br.bind('<<ComboboxSelected>>', self.on_select_bb)
        self.cb1 = ttk.Checkbutton(self.root,
                                   text='1st sensor',
                                   command=lambda: self.agreement_changed(),
                                   variable=self.agreement,
                                   onvalue='agree',
                                   offvalue='disagree').place(x=700, y=100)
        self.cb1 = ttk.Checkbutton(self.root,
                                   text='2nd sensor',
                                   command=lambda: self.agreement_changed(),
                                   variable=self.agreement,
                                   onvalue='agree',
                                   offvalue='disagree').place(x=790, y=100)
        self.reload = tk.Button(self.root, text='Reload', command=lambda:  self.reload_port()).grid(
            row=1, column=3, ipadx="10")
        self.Connect = tk.Button(self.root, text='Connect', command=lambda:  self.connect()).grid(
            row=1, column=4, ipadx="10")

    def select_port(self):
        print('test')

    def reload_port(self):
        self.cb = ttk.Combobox(self.root, values=self.serial_ports())
        self.cb.grid(row=1, column=1, ipadx="100")


def main():
    root = tk.Tk()
    program = ParentClass(root, 'MST')
    program.create_program(root)
    root.mainloop()




if __name__ == '__main__':
    main()
