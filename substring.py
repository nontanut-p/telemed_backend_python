string = "0x55 0xAA 0x04 0x02 0x00 0xF9"
string = string.replace("0x", "")
x = string.split()

print(x)

'''
ECG Detection(0x01): Enable/Disable ECG parameter output

ECG_ENABLE = ['55', 'AA', '04', '01', '01', 'F9']
ECG_DISABLE = ['55', 'AA', '04', '01', '00', 'FA']

NIBP Detection(0x02): Enable/Disable NIBP parameter output

NIBP_START = ['55', 'AA', '04', '02', '01', 'F8']
NIBP_STOP = ['55', 'AA', '04', '02', '00', 'F9']

SPO2 Detection(0x03)： Enable/Disable SPO2 parameter output

SPO2_ENABLE = ['55', 'AA', '04', '03', '01', 'F7']
SPO2_DISABLE = ['55', 'AA', '04', '03', '00', 'F8']

TEMP Detection(0x04)：Enable/Disable Temperature parameter output

TEMP_ENABLE = ['55', 'AA', '04', '04', '01', 'F6']
TEMP_DISABLE = ['55', 'AA', '04', '04', '00', 'F7']

NIBP Preset Cuff Pressure(0x0A)： Setup NIBP preset cuff pressure before new test
(0x55 0xAA 0x04 0x0A 0x96 0x5F)

NIBP_PRESET_CUFF = ['55', 'AA', '04', '0A', '96', '5F']

'''