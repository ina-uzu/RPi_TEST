import time
import string
import operator
import RPi.GPIO as GPIO
import serial
from smbus import SMBus

READ_RATE = 1.0

#For I2C
READ = 0x0
I2C = 0x1
CAL = 0x2
I = 0x3

DO_DATA_MAX_LENGTH=20
DO_TERMINATOR = 255
DO_ADDR = 0x63
bus = SMBus(1)

#For RS485 (UART)
BAUD_RATE = 22800
BRIX_DATA_LENGTH=13
BRIX_ADDR = 0x01
CRC_L = 0x44    
CRC_H = 0x0C
READ_CMD = [chr(BRIX_ADDR), chr(0x03), chr(0x00),chr(0x00), chr(0x00), chr(0x08), chr(CRC_L), chr(CRC_H)]
READ_CMD_STR = ''.join(READ_CMD)
ser = serial.Serial('/dev/serial0',BAUD_RATE, timeout=1)

class Master :
    def __init__(self):
        self.DATA = {'DO': '', 'BRIX_TEMP': '', 'BRIX_BRIX' : '' }
    
    def readDO(self):
        res=""
        data=""
        data = bus.read_i2c_block_data(DO_ADDR, READ, DO_DATA_MAX_LENGTH)
        
        for i in range(len(data)):
            if i==0:
                print("DO Response Code is %d" % int(data[i]))
                continue
            tmp = chr(data[i])
            if ord(tmp) ==DO_TERMINATOR: 
                break
            res += tmp
        self.DATA['DO'] = res

    def readBRIX(self):
        ser.write(READ_CMD_STR)
        data = []
    
        for i in range(BRIX_DATA_LENGTH):
            tmp = ser.read(1)
            try :
                data.append(ord(tmp))
            except :
                data.append(0)
        
        # Temperature
        tmp = data[3]
        for i in range(3):
            tmp = tmp << 4
            tmp = data[i+4]
        self.DATA['BRIX_TEMP']= "%f" % tmp
        
        # Brix
        tmp = data[7]
        for i in range(3):
            tmp = tmp << 4
            tmp = data[i+8]
        self.DATA['BRIX_BRIX'] = "%f" % tmp

    def getAllData(self):
        self.readDO()
        self.readBRIX()

        for k in sorted(self.DATA.keys()) :
            print("%s = %s" % ( k , self.DATA[k] ))
        print("")

    #For Next Test
    def sendAllData(self):
        pass

def main():
    READ_RATE = 1.0 
    master = Master() 
    
    print("1. Read")
    print("2. Rate")
    print("3. Cal")
    print("4. Quit")
    

    while True :
        cmd = raw_input("Command : ")

        if cmd == "Read" :
            print("Start Reading")
            print("Read Rate is %d" % READ_RATE)

            while True:
                try :
                    master.getAllData()
                    time.sleep(READ_RATE)
                except KeyboardInterrupt :
                    print("Stop reading")
                    break

        elif cmd == "Rate" :
            try:
                READ_RATE = float(raw_input('Enter new Read Rate '))
            except ValueError:
                print('Invalid Read Rate')
        
        elif cmd == "Cal" :
            pass
        elif cmd == "Quit" :
            break

if __name__ == '__main__' :
    main()
