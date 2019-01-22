import sys
import serial
import string
import time
from serial import SerialException

PORT = "/dev/serial0"
BAUD_RATE = 9600

def read_data():
	buf =[]
	while True :
		tmp = ser.read(1)
		if tmp =="\r":
			break;
		buf.append(tmp)
	res =''.join(buf)
	print("%s pH" % res)

def send_cmd(cmd):
	buf = cmd+'\r'
	try : 
		ser.write(buf.encode('utf-8'))
	except SerialException as e:
		print("Error : " , e)

def init():
	send_cmd("R")	
	while True :
		tmp = ser.read(1)
		if tmp =="\r":
			break;
	
if __name__ == "__main__":

	print("Opening Serial port")
	try : 
		ser = serial.Serial(PORT, BAUD_RATE, timeout=0)
	except serial.SerialException as e :
		print("Error : ", e)
		sys.exit(0)
	
	#Perfom a R cmd to handle the first garbage data
	init()

	print("1. R" )
	print("2. C,n")
	print("3. Cal")
	print("4. Quit")

	# Get command
	while True :
		cmd = raw_input("Command : ")
	
		if cmd == "Quit" :
			print("BYE~")
			break
		else :
			whatCmd = cmd.split(',')
			send_cmd(cmd)

			# Cont - Reading
			if whatCmd[0] == "C" :
				print("Start Reading")
				while True:
					try :
						time.sleep(0.8)
						read_data()
					except KeyboardInterrupt :
						send_cmd("C,0")
						break
			
			# 1 Reading 
			elif whatCmd[0] =="R" :
				time.sleep(0.8)
				read_data()

			elif whatCmd[0]=="Cal" :
				print ("Calibration done")
