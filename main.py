from os import read
import serial
import keyboard
import time
open_program = seconds = time.time()



TEMP_ENABLE = ['04', '04', '01', 'F6'] # T
TEMP_DISABLE = ['04', '04', '00', 'F7'] 
SPO2_ENABLE = ['04', '03', '01', 'F7'] # S
SPO2_DISABLE = ['04', '03', '00', 'F8']
NIBP_PRESET_CUFF = ['04', '0A', '96', '91'] # N
NIBP_START = ['04', '02', '01', 'F8'] # N
NIBP_STOP = ['04', '02', '00', 'F9']
ECG_ENABLE = ['04', '01', '01', 'F9'] # E
ECG_DISABLE = ['04', '01', '00', 'FA']
ECG_WAVE_DISABLE = ['04', 'FB', '00', '00']    
SPO2_WAVE_DISABLE  = ['04' , 'FE', '00', 'FD']
RESP_WAVE_DISABLE  = ['04' , 'FF', '00', 'FC']

class VitalSignDevice:
    NIBP_DICT = {
        'Status': "", 
        'Cuff Pressure': 0,
        'Sys Pressure': 0, 
        'Mean Pressure': 0,
        'Dia Pressure': 0
    }
    int_temp = 0
    decimal_temp = 0
    def __init__(self, COMPORT):
        self.COMPORT = COMPORT
        self.ser = serial.Serial(self.COMPORT, 115200)
        if self.ser.is_open:
            print(f'CONECTING TO {self.COMPORT}')
            self.writeFunction(TEMP_DISABLE)
            self.writeFunction(SPO2_DISABLE)
            self.writeFunction(ECG_DISABLE)
            self.writeFunction(ECG_WAVE_DISABLE)
            self.writeFunction(SPO2_WAVE_DISABLE)
            self.writeFunction(RESP_WAVE_DISABLE)
            self.writeFunction(NIBP_STOP)
        else : print("!!! Can't open this port : !!!")
 
    def writeFunction(self, func):
        self.ser.write(bytes.fromhex('55')) 
        self.ser.write(bytes.fromhex('AA'))    
        for hex in func:
            self.ser.write(bytes.fromhex(hex))

    def temp_senosor(self,data_lenght):
        temp_data = {
            "Status": "No status",
            "Temp_int": 0,
            "Temp_decimal": 0
            }
        sensor_status = 0
        for i in range(data_lenght):
            read_serial = self.ser.read()
            data = ord(read_serial)
            #print(f' i : {i} , {read_serial} , decoding {data} {type(data)}')
            if i == 0:
                sensor_status = data
                if data == 0:
                    temp_data['Status'] = 'Normal'
                elif data == 1:
                    temp_data['Status'] = 'TEMP sensor is off' 
            elif i == 1:
                #print(data)
                if data != 0:
                    temp_data['Temp_int'] = data
            elif i == 2:
                #print(data)
                if data != 0:
                    temp_data['Temp_decimal'] = data / 10
        if sensor_status == 0:
            seconds = time.time() - open_program 
            return print(temp_data['Temp_int']+temp_data['Temp_decimal'], 'C Time : ' , seconds )
        else: return print(temp_data['Status'])
    def nibp(self, data_lenght):

        for i in range(data_lenght):
            read_serial = self.ser.read()
            data = ord(read_serial)
            #print(data , read_serial)  
            if i == 0 :
                binaray = bin(data)
                '''
                    NIBP_DICT = {
                        'Status': "", 
                        'Cuff Pressure': 0,
                        'Sys Pressure': 0, 
                        'Mean Pressure': 0,
                        'Dia Pressure': 0
                    }
                '''
            elif i == 1 :
                self.NIBP_DICT['Cuff Pressure'] = data
                print(f' Cuff Pressure {data}')
            elif i == 2 :
                if data != 0 :
                    self.NIBP_DICT['Sys Pressure'] = data
            elif i == 3 :
                if data != 0:
                    self.NIBP_DICT['Mean Pressure'] = data 
            elif i == 4 :
                if data != 0:
                    self.NIBP_DICT['Dia Pressure'] = data 
                return print(f" Cuff Pressure: {self.NIBP_DICT['Cuff Pressure']} Sys Pressure {self.NIBP_DICT['Sys Pressure']} Mean Pressure {self.NIBP_DICT['Mean Pressure']}  Dia Pressure {self.NIBP_DICT['Dia Pressure']} " )


    def spo2(self,data_lenght):
        SPO2_DATA = {
            "Status": "No status",
            "%SPO2": 0,
            "Pulse_Rate": 0
            }
        sensor_status = 0
        for i in range(data_lenght):
            read_serial = self.ser.read()
            data = ord(read_serial)
            #print(f' i : {i} , {read_serial} , decoding {data} {type(data)}')
            if i == 0:
                sensor_status = data
                if data == 0:
                    SPO2_DATA['Status'] = 'Sensor is normal'
                elif data == 1:
                    SPO2_DATA['Status'] = 'Sensor is off'
                elif data == 2:
                    SPO2_DATA['Status'] = 'No finger insert'
                elif data == 3:
                    SPO2_DATA['Status'] = 'Searching pulse signal'                    
                else : SPO2_DATA['Status'] = 'Searching timeout'  
            elif i == 1:
                if data != 127:
                    SPO2_DATA['%SPO2'] = data
            elif i == 2:
                if data != 255:
                    SPO2_DATA['Pulse_Rate'] = data

        ''' A2 : 00 Normal,  01 sensor is off , 02 no finger insert , 03 searching pulse signal 04 searching timeout'''
        ''' A3 : 0 - 100 % O2 '''
        ''' A4 Pulse Rate '''
        if sensor_status == 0 :
            seconds = time.time() - open_program 
            return print(f' SPO2 {SPO2_DATA["%SPO2"]}%  Pulse Rate {SPO2_DATA["Pulse_Rate"]} bpm {seconds}' )
        
        else : 
            return print(SPO2_DATA["Status"])
    def sensor_call(self,sensor_id,data_lenght):
        #sensor_id 
        deta_lenght = data_lenght
        if sensor_id == '05':
            print(f'Sensor is Temp')
            self.temp_senosor(data_lenght)
        elif sensor_id == '04':
            print(f'Sensor is SPO2')
            self.spo2(data_lenght)
        elif sensor_id == '03':
            print(f'Sensor is NIBP')
            self.nibp(data_lenght)

    def recive_data(self):
        
        read_serial = self.ser.read().hex()
        #print(read_serial , 'HEX')
        read_serial = str(read_serial)
        if read_serial == "aa":
            print('----------------------------------------------------')
            read_serial = str(self.ser.read())[4:-1]
            try:
                if int(read_serial[0:1]) == 0 :
                    data_lenght = int(read_serial[1:2]) - 2
                else : data_lenght = int(read_serial)
                #print(f'lenght data is {read_serial} ')
                sensor_id = str(self.ser.read())[4:-1]   
                #print('sensor id :', sensor_id)
                self.sensor_call(sensor_id,data_lenght)
            except: print('error')
        return 0   
            #self.message_lenght = int(read_serial)
        


#device.initailFunction()
Temp_Detection_Status = 0 
recive_data = 0

def main():
    device = VitalSignDevice('COM5')
    global Temp_Detection_Status , recive_data
    #device.writeFunction(NIBP_PRESET_CUFF)
    #device.writeFunction(NIBP_START)
    #device.writeFunction(TEMP_ENABLE)
    #device.writeFunction(NIBP_START)
    while True:
      
        device.writeFunction(SPO2_ENABLE)  
        device.recive_data()
          
        if keyboard.is_pressed("Esc"):
            print('STOP PROGRAME')
            break
        elif keyboard.is_pressed('E'):
            print('Stop NIBP')
            device.writeFunction(NIBP_STOP)
            break
        '''
        elif keyboard.is_pressed("C"): ## Command Menu
            input_command = input('Please input sensor/function name (ECG,NIBP,SPO2,TEMP,Data) :')
            if input_command.lower() == 'ecg' :
                input_command = input('Enable/Disable : ')
                if input_command.lower() == 'enable':
                    device.writeFunction(ECG_ENABLE)
                else : device.writeFunction(ECG_DISABLE)
            elif input_command.lower() == 'spo2':
                input_command = input('Enable/Disable : ')  
                if input_command.lower() == 'enable':
                    device.writeFunction(SPO2_ENABLE)
                else : device.writeFunction(SPO2_DISABLE)
            elif input_command.lower() == 'temp':
                input_command = input('Enable/Disable : ')  
                if input_command.lower() == 'enable':
                    device.writeFunction(TEMP_ENABLE)
                else : device.writeFunction(TEMP_DISABLE)  
            elif input_command.lower() == 'data':
                input_command = input('START or STOP : ')
                if input_command.lower() == 'start':
                    recive_data = 1 
                    print('Program started')
                else : recive_data = 0                           
        else:
            continue
        '''
        
        
        
main()
        
'''
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

'''