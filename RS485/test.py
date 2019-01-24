import serial
import time
import RPi.GPIO as GPIO

rate = 22800
ser = serial.Serial("/dev/ttyS0", rate, timeout=1)
print(ser)

while True :
    ch = ser.read(1)
    print(ch)
    time.sleep(0.5)

