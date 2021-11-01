import serial
import time 
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


TEMP_ENABLE = ['04', '04', '01', 'F6']
TEMP_DISABLE = ['04', '04', '00', 'F7']
SPO2_ENABLE = ['04', '03', '01', 'F7']
SPO2_DISABLE = ['04', '03', '00', 'F8']
NIBP_PRESET_CUFF = ['04', '0A', '96', '5F']
NIBP_START = ['04', '02', '01', 'F8']
NIBP_STOP = ['04', '02', '00', 'F9']
ECG_ENABLE = ['04', '01', '01', 'F9']
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
    
    def __init__(self, COMPORT):
        self.COMPORT = COMPORT
        self.ser = serial.Serial('/dev/ttyUSB0', 115200)
        if self.ser.is_open:
            print(f'CONECTING TO {COMPORT}')
            self.writeFunction(ECG_WAVE_DISABLE)
            self.writeFunction(SPO2_WAVE_DISABLE)
            self.writeFunction(RESP_WAVE_DISABLE)
            self.writeFunction(NIBP_STOP)
            #(0x55 0xAA 0x04 0x04 0x01 0xF6) ENABLE TEMP
           # self.ser.write(bytes.fromhex('55'))
           # self.ser.write(bytes.fromhex('AA'))
           # self.ser.write(bytes.fromhex('04'))
           # self.ser.write(bytes.fromhex('04'))
           # self.ser.write(bytes.fromhex('01'))
           # self.ser.write(bytes.fromhex('F6'))
        else : print("Can't open")
 
    def writeFunction(self, func):
        print(f'{func} !!')
        #0x55 0xAA
        self.ser.write(bytes.fromhex('55')) 
        self.ser.write(bytes.fromhex('AA'))    
        for hex in func:
            self.ser.write(bytes.fromhex(hex))
            print(hex)
    def initailFunction(self):
        '''Disable ECG parameter output '''
        # 0x55 0xAA 0x04 0x01 0x00 0xFa
        ECG_PARAM_DISABLE = bytes.fromhex("0x55 0xAA 0x04 0x01 0x00 0xFa")
        #self.ser.write(ECG_PARAM_DISABLE)
        print(ECG_PARAM_DISABLE)

    def multiple(self):
        read_serial = str(self.ser.read())[2:-1]
        print(read_serial)
        if read_serial == "xaa":
            read_serial = str(self.ser.read())[3:-1]
            print(f'{read_serial}')
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

#device.writeFunction(TEMP_ENABLE)
device.writeFunction(ECG_DISABLE)
while True : 
    device.multiple()
 

    '''
TEMP_ENABLE = ['04', '04', '01', 'F6']
TEMP_DISABLE = ['04', '04', '00', 'F7']
SPO2_ENABLE = ['04', '03', '01', 'F7']
SPO2_DISABLE = ['04', '03', '00', 'F8']
NIBP_PRESET_CUFF = ['04', '0A', '96', '5F']
NIBP_START = ['04', '02', '01', 'F8']
NIBP_STOP = ['04', '02', '00', 'F9']
ECG_ENABLE = ['04', '01', '01', 'F9']
ECG_DISABLE = ['04', '01', '00', \xaa'FA']
   
    
    '''