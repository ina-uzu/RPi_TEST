import smbus
import io
from io import open
import string
import fcntl

SLAVE_ADDR = 0x703
ADDR = 0x01

'''
file_read = io.open("/dev/i2c-1", "rb", buffering=0)
file_write = io.open("/dev/i2c-1", "wb", buffering=0)
'''

bus = smbus.SMBus(1)

cmd = raw_input("CMD: ")
cmd = list(cmd)

for i in range(len(cmd)) :
	bus.write_byte(ADDR,ord(cmd[i]))

