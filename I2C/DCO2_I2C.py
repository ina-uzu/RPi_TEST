import time
import string
import sys
import os
from smbus import SMBus

#command 
START = 0x23
END = 0x21
READ = 0x57
CAL = 0x31

#Read Rate
READ_RATE = 1.0
READ_BYTE_NUM=7

#I2C Address / Bus
ADDR = 0x31
READ_ADDR = 0x31
WRITE_ADDR = 0x31

#status
BUSY = 0x0
FREE = 0x1

bus = SMBus(1)

def main():
        print("1. Read")
        print("2. Cal")
        print("3. Quit")

        READ_RATE=1.0
	while True :
		cmd = raw_input("Command : ")
	
		#request for reading
		if cmd == 'Read':
			print("Start reading (Stop : Ctrl + c )")
			print("Read-Rate is %.2f "% READ_RATE)
			#read.readStart()

			try:
				while True :
					send_read_cmd()
					time.sleep(READ_RATE)

			except KeyboardInterrupt :
					print("Stop reading")
		
		#Calibration
		elif cmd == 'Cal':
			res = send_cal_cmd()	
			if res == 1:
				print("Calibration done!")
			else :
				print("Calibration failed!")

		#quit
		elif cmd == 'Quit':
			print("BYE~~")
			os._exit(1)
			break;

		else:
			print("Wrong commnand")

def send_cal_cmd():
	#send start signal & check response
	while bus.write_byte(ADDR, START) == BUSY :
		pass

	#send READ cmd 
	bus.write_byte(WRITE_ADDR , CAL )
	
	#send stop signal 
	bus.write_byte(ADDR, END)


	#send start signal & check response
	while bus.write_byte(ADDR, START) == BUSY :
		pass

	#receive data (7-byte) from sensor
	data = bus.read_byte(READ_ADDR)
					
	return data

def send_read_cmd() :
	#send start signal & check response
	while bus.write_byte(ADDR, START) == BUSY :
		pass

	#send READ cmd 
	bus.write_byte(WRITE_ADDR , READ)
		
	#send stop signal 
	bus.write_byte(ADDR, READ)

	#send start signal & check response
	while bus.write_byte(ADDR, START) == BUSY :
		pass

	#receive data (7-byte) from sensor
	data = bus.read_i2c_block_data(READ_ADDR,0, READ_BYTE_NUM)
					
	res = data[1] << 8
	res += data[2] 
						
	#write the data 
	print("%d ppm" % res)
		
if __name__=='__main__' :
	main()
