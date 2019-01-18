import serial

ser = serial.Serial("/dev/ttyAMA0", 9600)
print(ser.portstr)
ser.write("hello")
ser.write("hello")
ser.write("hello")

ser.close()
