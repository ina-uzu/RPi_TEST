import time
import string
import threading 
import sys
import os
from smbus import SMBus

#command 
READ = 0x0	
I2C = 0x1	
CAL = 0x2
I = 0x3

#Read Rate
READ_RATE = 1.0
DATA_MAX_LENGTH = 20
TERMINATOR = 255

#I2C Address / Bus
PH_ADDR = 0x64
bus = SMBus(1)

def main():
        print("1.Read")
        print("2.Rate")
        print("3.I2C Address Check")
        print("4.Cal")
        print("5.Quit")

	READ_RATE=1.0
	while True :
		cmd = raw_input("Command : ")
	
		if cmd =='Help':
			print("Read / Rate / I2C / Cal / Quit")

		#request for reading
		elif cmd == 'Read':
			print("Start reading (Stop : Ctrl + c )")
			print("Read-Rate is %.2f "% READ_RATE)
			#read.readStart()

			try:
				while True :
					#send READ cmd to the sensor & receive data from sensor
					global res
					res="" 
					data = bus.read_i2c_block_data(PH_ADDR,READ,DATA_MAX_LENGTH)
					for i in range(len(data)):
						if i == 0:
							print("Response Code is %d" % int(data[i]))
							continue
						tmp = chr(data[i])
                                                if ord(tmp) == TERMINATOR:
                                                    break    
                                                '''
						if tmp !='.' and (tmp <'0' or tmp >'9'):
							break
						'''
                                                res += tmp
					
					#write the data 
					print("%s pH" % res)
					data=""

					#sleep
					time.sleep(READ_RATE)

			except KeyboardInterrupt :
					print("Stop reading")
		
		elif cmd == 'Rate':
			new_rate_str = raw_input("Enter New Reading Rate : ")
			
			#Check input value (must be float type)
			try :
				READ_RATE = float(new_rate_str)
			except ValueError:
				print("Invalid Rate")

		#change the i2c address
		elif cmd == 'I2C':
			data = bus.read_i2c_block_data(PH_ADDR,I2C,5)
			addr=""
			for i in range(len(data)):
				if i == 0:
					print("Response Code is %d" % int(data[i]))
					continue
				tmp = chr(data[i])
				if tmp <'0' or tmp >'9':
					break
				addr += tmp
			
			print("I2C addr is %s" % addr)
		
		#Check the I2C address
		elif cmd == 'I':
			new_addr = input("Enter New Address :")
			if new_addr >0xff or new_addr<0 :
				print("Invalid Address")
			else :
				bus.write	
				bus.write_byte(PH_ADDR, new_addr)
				#addr= new_addr

		#Calibration
		elif cmd == 'Cal':
			bus.write_byte(PH_ADDR, CAL)
                        code = bus.read_byte(PH_ADDR)
                        print("Response Code is %d" % code)
			print("Calibration done!")

		#quit
		elif cmd == 'Quit':
			print("BYE~~")
			os._exit(1)
			break;

		else:
			print("Wrong commnand")


# NO USE
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
		self.f= open("data_pH.txt", "a")

		#send READ cmd to the sensor
		bus.write_byte(PH_ADDR,READ)
		
		#receive data from sensor
		global res
		res="" 
		data = bus.read_i2c_block_data(PH_ADDR,0,DATA_MAX_LENGTH)
		
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
