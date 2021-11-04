from os import read
import serial
import time 
import tkinter as tk
from tkinter import Message, ttk
import keyboard

'''
class VitalSignDevice(comport):
    """docstring for ."""

    def __init__(self, comport):
        super(, self).__init__()
        ser = serial.Serial(comport , 115200)
    def
import serial
port = "/dev/ttyAMAO"
usart = serial.Serial (port,4800)
message_bytes = bytes.fromhex("0111050200013F0804")
usart.write(message_bytes)
'''
Enable_temp = []
## (0x55 0xAA 0x04 0x08 0x02 0xF1)

TEMP_ENABLE = ['04', '04', '01', 'F6'] # T
TEMP_DISABLE = ['04', '04', '00', 'F7'] 
SPO2_ENABLE = ['04', '03', '01', 'F7'] # S
SPO2_DISABLE = ['04', '03', '00', 'F8']
NIBP_PRESET_CUFF = ['04', '0A', '96', '5F'] # N
NIBP_START = ['04', '02', '01', 'F8'] # N
NIBP_STOP = ['04', '02', '00', 'F9']
ECG_ENABLE = ['04', '01', '01', 'F9'] # E
ECG_DISABLE = ['04', '01', '00', 'FA']
ECG_WAVE_DISABLE = ['04', 'FB', '00', '00']    
SPO2_WAVE_DISABLE  = ['04' , 'FE', '00', 'FD']
RESP_WAVE_DISABLE  = ['04' , 'FF', '00', 'FC']
#(0x55 0xAA 0x04 0xFF 0x00 0xFC)
#(0x55 0xAA 0x04 0xFE 0x00 0xFD
#0x55 0xAA 0x04 0x01 0x00 0xFA
#(0x55 0xAA 0x04 0xFB 0x00 0x00
#0x55 0xAA 0x04 0xFF 0x00 0xFC

class VitalSignDevice:
    int_temp = 0
    decimal_temp = 0
    def __init__(self, COMPORT):
        self.COMPORT = COMPORT
        self.ser = serial.Serial('/dev/ttyUSB0', 115200)
        if self.ser.is_open:
            print(f'CONECTING TO {self.COMPORT}')
            self.writeFunction(TEMP_DISABLE)
            self.writeFunction(SPO2_DISABLE)
            self.writeFunction(ECG_DISABLE)
            self.writeFunction(ECG_WAVE_DISABLE)
            self.writeFunction(SPO2_WAVE_DISABLE)
            self.writeFunction(RESP_WAVE_DISABLE)
            self.writeFunction(NIBP_STOP)
        else : print("Can't open")
 
    def writeFunction(self, func):
        #print(f'{func} !!')
        #0x55 0xAA
        self.ser.write(bytes.fromhex('55')) 
        self.ser.write(bytes.fromhex('AA'))    
        for hex in func:
            self.ser.write(bytes.fromhex(hex))
            #print(hex)
    def initailFunction(self):
        '''Disable ECG parameter output '''
        # 0x55 0xAA 0x04 0x01 0x00 0xFa
        ECG_PARAM_DISABLE = bytes.fromhex("0x55 0xAA 0x04 0x01 0x00 0xFa")
        #self.ser.write(ECG_PARAM_DISABLE)
        print(ECG_PARAM_DISABLE)

    def sensor_function(self,sensor_id,data_lenght):
        #sensor_id 
        data_lenght = data_lenght
        if(sensor_id == '05'):
            print('sensor id :', sensor_id , ' Temp Detection')
            print('data_lenght',data_lenght)
            
            for i in range(data_lenght):
                if i == 1 : 
                    read_serial = str(self.ser.read())[4:-1]
                    
                    hex = read_serial
                    if hex != '' :
                        self.decimal_temp = int(hex, 16)
                        print(read_serial, 'int', self.decimal_temp)
                    else:  print(read_serial, 'error' , self.decimal_temp)
                    
                elif i == 2:
                    read_serial = str(self.ser.read())[5:-1]
                    print(read_serial, 'decimal', )
                    hex = read_serial
                    if hex == ' ':
                        print('empty')
                    if hex != '' :
                        decimal_temp = int(read_serial) / 10
                        #dec_temp = int(hex, 16)
                        #print(read_serial, 'dec', )
                        

                else : 
                    read_serial = str(self.ser.read())[5:-1]
                    print(read_serial)
                    
                
        elif (sensor_id =='03'):
            print('SPO2 Dectection')
       # return print(f'Temp is {dec_temp + decimal_temp}')

    def recive_data(self):
        print('----------------------------------------------------')
        read_serial = str(self.ser.read())[3:-1]
        print(read_serial)
        if read_serial == "xaa":
            read_serial = str(self.ser.read())[4:-1]
            if int(read_serial[0:1]) == 0 :
                data_lenght = int(read_serial[1:2]) - 2
            else : data_lenght = int(read_serial)
            #print(f'lenght data is {read_serial} ')
            sensor_id = str(self.ser.read())[4:-1]   
            #print('sensor id :', sensor_id)
            self.sensor_function(sensor_id,data_lenght)
           
            #self.message_lenght = int(read_serial)
        
'''
b'U'
b'\xaa'
b'\x08'
b'\x02'
b'\x00'
b'\x19'
b'\t'
b'\x00'
b'\x00'
b'\xd0'
b'U'

'''


device = VitalSignDevice('/ttyUSB0')
#device.initailFunction()

device.writeFunction(TEMP_ENABLE)

while True:
    if keyboard.is_pressed("Esc"):
        print("You pressed p")
        break
    else:
        device.recive_data()
    '''
TEMP_ENABLE = ['04', '04', '01', 'F6']
TEMP_DISABLE = ['04', '04', '00', 'F7']
SPO2_ENABLE = ['04', '03', '01', 'F7']
SPO2_DISABLE = ['04', '03', '00', 'F8']
NIBP_PRESET_CUFF = ['04', '0A', '96', '5F']
NIBP_START = ['04', '02', '01', 'F8']
NIBP_STOP = ['04', '02', '00', 'F9']
ECG_ENABLE = ['04', '01', '01', 'F9']
ECG_DISABLE = ['04', '01', '00', 'FA']
  
    '''