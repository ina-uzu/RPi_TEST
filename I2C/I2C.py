import time
import string
import threading 
import sys
import os
from smbus import SMBus

import io
from io import open
import fcntl

#command 
READ = 0x0
I2C = 0x1
CAL = 0x2
I = 0x3

#I2C Address / Bus
addr = 0x01
bus = SMBus(1)
def main():
	read =CmdRead()


	while True :
		cmd = raw_input("Command : ")
	
		if cmd =='Help':
			print("Start / Stop / Rate / I2C / Cal ")

		#request for reading
		elif cmd == 'Start':
			print("Start reading")
			read.readStart()

		elif cmd == 'Stop':
			print("Stop reading")
			read.readStop()

		elif cmd == 'Rate':
			new_rate = input("Enter New Reading Rate : ")
			read.changeReadRate(new_rate)

		#change the i2c address
		elif cmd == 'I2C':
			bus.write_byte(addr, I2C)
			cur_addr = bus.read_byte(addr)
			print("I2C addr is %x" % cur_addr)

		#Check the I2C address
		elif cmd == 'I':
			new_addr = input("Enter New Address :")
			if new_addr >0xff or new_addr<0 :
				print("Invalid Address")
			else :
				bus.write_byte(addr, I)	
				bus.write_byte(addr, new_addr)
				#addr= new_addr

		#Calibration
		elif cmd == 'Cal':
			bus.write_byte(addr, CAL)
			res = bus.read_byte(addr)
		
			if res == 1:
				print("Calibration done!")
			else :
				print("Calibration failed!")

		#quit
		elif cmd == 'quit':
			print("BYE~~")
			os._exit(1)
			break;

		else:
			print("Wrong commnand")


class CmdRead :	

	def __init__(self) :
		self.RATE = 1
		self.readTimer = None
		self.f = None
		pass
	
	def __del__(self) :
		if self.f is not None :
			self.f.close()
		if self.f is not None :
			self,readTimer.cancel()
		
	def readStart(self):
		#open data file
		self.f= open("data_DO.txt", "a")

		#send READ cmd to the sensor
		bus.write_byte(addr,READ)
		
		#receive data from sensor
		global res
		res="" 
		data = bus.read_i2c_block_data(addr,0, 32)
		
		for i in range(len(data)):
			tmp = chr(data[i])

			if tmp !='.' and (tmp <'0' or tmp >'9'):
				break;
			res += tmp
		
		#write the data 
		res += "\n"
		self.f.write(res)
		data=""
		
		self.readTimer = threading.Timer(self.RATE, self.readStart).start()

	def readStop(self):
		if self.f is not None :
			self.f.close()

		if self.readTimer is not None :
			self.readTimer.cancel()

	def changeReadRate(self,new_rate):
		self.RATE = new_rate

	def kill(self) :
		del self

		
if __name__=='__main__' :
	main()
