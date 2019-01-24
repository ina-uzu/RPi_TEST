import serial
import string
import time
import RPi.GPIO as GPIO

BAUD_RATE = 22800
READ_RATE = 1
DATA_LENGTH =13

#Can be changed
ADDR = 0x01
CRC_L = 0x44
CRC_H = 0x0C
READ_CMD = [chr(ADDR),chr(0x3), chr(0x00) ,chr(0x00),chr(0x00),chr(0x08), chr(CRC_L), chr(CRC_H)]
READ_CMD_STR = ''.join(READ_CMD)


def readData():
    ser.write(READ_CMD_STR)
    data=[]
        
    for i in range(DATA_LENGTH):
        tmp = ser.read(1)
        try :
            data.append(ord(tmp))
        except :
            data.append(0)
        
    temp = data[3]
    for i in range(3):
        temp = temp << 4
        temp = data[i+4]
    print("Temp is %f" % temp)

    temp = data[7]
    for i in range(3):
        temp = temp << 4
        temp = data[i+8]
    print("Brix is %f" % temp)
    print("")

#CODE
ser = serial.Serial("/dev/ttyS0", BAUD_RATE, timeout=1)

print("1.Read")
print("2.Rate")
print("2.Quit")

while True:
    cmd = raw_input("Command: ")

    if cmd =="Read" :
        print("Start Reading")
        print("Read Rate is %f" % READ_RATE)
        while True:
            try :
                readData()
                time.sleep(READ_RATE)
            except KeyboardInterrupt:
                print("Stop Reading")
                break
    elif cmd =="Rate":
        rate = raw_input("Enter New Read Rate : ")
        try: 
            READ_RATE = float(rate)
        except ValueError as e:
            print("Invaild Read Rate")

    elif cmd == "Quit":
        break


