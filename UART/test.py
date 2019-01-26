import serial

ser = serial.Serial('/dev/serial0', 9600, timeout=1)

while True:
	cmd = raw_input("R or W ?")

	if cmd =="R" :
		if ser.inWating() :
			read_str = ""
			while True:
				data = ser.read(1)
				if data == "\n" :
					break
				read_str += tmp
			print(read_str)
				
	elif cmd =="W":
		ser.write("I'M PI")

