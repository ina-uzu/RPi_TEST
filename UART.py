import serial

ser = serial.Serial("/dev/serial0", 9600, timeout=1)
print(ser.portstr)

ser.write("TEST START")

while True :
	cmd = raw_input("R or W ? (Q - quit)")
	if cmd =='R' :
		while 1:
			if ser.in_waiting >0 :
				res = ser.read(1).rstrip('\x00')	
				if len(res) > 0 :
					print(len(res))

				if res=='\n' :
					break
	elif cmd=='W':
		data = raw_input("Enter MSG :")
		ser.write(data)
	
	elif cmd=='Q':
		ser.close()
		break
	else:
		print("Wrong Command")
		

