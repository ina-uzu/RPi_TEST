import sys
import serial
import string
import time
from serial import SerialException

PORT = "/dev/serial0"
BAUD_RATE = 9600

def read_data():
	buf =[]
	cnt=0
	
	while True :
		tmp = ser.read(1)
		print tmp
		if tmp == " " and cnt<2:
			cnt = cnt+1
			continue

		if tmp =="\n":
			break;
		buf.append(tmp)

	res =''.join(buf)
	print("%s" % res)

if __name__ == "__main__":

	print("Opening Serial port")
	try : 
		ser = serial.Serial(PORT, BAUD_RATE, timeout=0)
	except serial.SerialException as e :
		print("Error : ", e)
		sys.exit(0)
	
	print("1. Read" )
	print("3. Cal")
	print("4. Quit")

	# Get command
	while True :
		cmd = raw_input("Command : ")
	
		if cmd == "Quit" :
			print("BYE~")
			break
			
		#Reading 
		elif cmd =="Read" :
			print("Start Reading ( Stop : Ctrl+C )")
			while True :
				try:
					read_data()
					time.sleep(1)
				except KeyboardInterrupt :
					print("Stop Reading")
					break

		elif cmd =="Cal" :
			print ("Calibration done")
