#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <wiringPi.h>
#include <wiringSerial.h>

int main(){
	int fd, data;

	fd = serialOpen("/dev/ttyS0", 9600);

	if( fd<0){
		printf("Unable to open serial device : %s\n", strerror(errno));
		return 0;
	}

	printf("UART TEST\n");

	while(1){
		data = serialGetchar(fd);
		if( data==0)
			continue;
		printf("Received data :%c!\n", data);
		serialPutchar(fd, data);
		serialPuts(fd, "\n");
		fflush(stdout);
	}

	return 1;
}
