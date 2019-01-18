import time
import string
from smbus import SMBus

READ = 0x0
I2C = 0x1
CAL = 0x2
I = 0x3

addr = 0x63
c = 0x0
bus = SMBus(1)

#Enter command

while True :
	cmd = raw_input("Command : ")
	
	if cmd =='Help':
		print("R - read / I2C - get i2c addr / Cal - calibration")

	#request for 1-reading
	elif cmd == 'R':
		bus.write_byte(addr,READ)
		
		#while True:
		#next_char= bus.read_byte(addr)
		#res.append(next_char)

		global res
		res="" 
		data = bus.read_i2c_block_data(addr,0, 15)
		
		for i in range(len(data)):
			tmp = chr(data[i])
			if tmp !='.' and (tmp <'0' or tmp >'9'):
				break;
			res += tmp

		print("%s ppm" % res )
		data=""
		
	#change the i2c address
	elif cmd == 'I2C':
		bus.write_byte(addr, I2C)
		cur_addr = bus.read_byte(addr)
		print("I2C addr is %x" % cur_addr)

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
		
		if res ==0x1:
			print("Calibration done!")
		else :
			print("Calibration failed!")


	elif cmd == 'quit':
		print("BYE~~")
		break;

	else:
		print("Wrong commnand")

