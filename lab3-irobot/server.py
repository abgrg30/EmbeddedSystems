##This Code is for Server for iRobot Control through BeagleBone in Python.
##Course: CSE291E ( Robotics/Embedded Systems)
##Lab: 3
##Last Modified: 20-Nov-2015
##Team: CodeIT
##Developers: Abhinav Garg; Abhijit Tripathi; Pulkit Bhatnagar
##University of California, San Diego

import Adafruit_BBIO.UART as UART
import socket
import serial
import sys
from time import sleep

##Definitions of iRobot Create OpenInterface Command Numbers
##See the Create OpenInterface manual for a complete list
 
 
##                Create Command              // Arguments
Start = 128;
SafeMode = 131;
FullMode = 132;
Drive = 137;                ## 4:   [Vel. Hi] [Vel Low] [Rad. Hi] [Rad. Low]
DriveDirect = 145;          ## 4:   [Right Hi] [Right Low] [Left Hi] [Left Low]
Demo = 136;                 ## 2:    Run Demo x
Sensors = 142;              ## 1:    Sensor Packet ID
CoverandDock = 143;         ## 1:    Return to Charger
SensorStream = 148;         ## x+1: [# of packets requested] IDs of requested packets to stream
QueryList = 149;            ## x+1: [# of packets requested] IDs of requested packets to stream
StreamPause = 150;          ## 1:    0 = stop stream, 1 = start stream
PlaySong = 141;
Song = 140;
## iRobot Create Sensor IDs
BumpsandDrops = 7;
Distance = 19;
Angle = 20;
 
speed_left =  200;
speed_right = 200;

###############################################################

#UART.setup("UART1")
HOST = ''   # all available interfaces
PORT = 5000 # TCP/IP port


ser = serial.Serial(port='/dev/ttyO1', baudrate=57600, timeout=1.0)#, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)

if ser < 0:
	print 'Server UART Creation Failed!!'
else:
	print 'Server UART Created, fd = ' + str(ser)
	
ser.close()
ser.open()
if ser.isOpen():
	print 'Server Serial Ready'
else:
	print 'Server Serial Closed??'

def move():
	ser.flush()
##START Sequence  
    	ser.write(chr(Start))     ##128
    	ser.write(chr(SafeMode))  ##131
    	sleep(.5)
    	ser.write(chr(SensorStream))  ##148
    	ser.write(chr(1).encode())         ##1
    	ser.write(chr(BumpsandDrops)) ##7
    	sleep(.5)
##forward
    	ser.write(chr(DriveDirect))
    	ser.write(chr((speed_right>>8)&0xFF))
    	ser.write(chr(speed_right&0xFF))
    	ser.write(chr((speed_left>>8)&0xFF))
    	ser.write(chr(speed_left&0xFF))

def stop():
        ser.flush()
	
##	var= chr(DriveDirect)
##	var = var+chr(0)
##	var = var+chr(0)
##	var = var+chr(0)
##	var = var+chr(0)

	
	ser.write(chr(DriveDirect))
        ser.write(chr(0))
        ser.write(chr(0))
        ser.write(chr(0))
        ser.write(chr(0))

        
def turn_left():
        ser.flush()
        
    	ser.write(chr(DriveDirect))
    	ser.write(chr((speed_right>>8)&0xFF))
    	ser.write(chr(speed_right&0xFF))
    	ser.write(chr(((-speed_left)>>8)&0xFF))
    	ser.write(chr((-speed_left)&0xFF))


def turn_right():
        ser.flush()
        
	ser.write(chr(DriveDirect))
    	ser.write(chr(((-speed_right)>>8)&0xFF))
    	ser.write(chr((-speed_right)&0xFF))
    	ser.write(chr((speed_left>>8)&0xFF))
    	ser.write(chr(speed_left&0xFF))



def serialread(rec):

	chunk = ser.read(100)
	
	if chunk == '':
		print 'Server UART read failed for :' + rec
	else:
		print 'Server UART data : ' + chunk
		
	return chunk
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if s < 0:
	print 'Server Socket Creation Failed!!'
else:
	print 'Server Socket Created, fd = ' + str(s)
 
try:
    s.bind((HOST, PORT)) #Bind socket to local host and port
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

s.listen(10)  #Start listening on socket
print 'Socket now listening'

conn, addr = s.accept()  #wait to accept a connection - blocking call
print 'Connected with ' + addr[0] + ':' + str(addr[1])

#now keep talking with the client
while 1:
	
	rec = conn.recv(100)

	if rec == '':
		print 'Server Receive Failed!!'
	else:
		print 'Server Data Received = ' + rec
		
		if rec == '1':
			print 'Move Forward'
			move()			
		elif rec == '2':
			print 'Stop Robot'
			stop()
		elif rec == '3':
			print 'Turn Left'
			turn_left()
		elif rec == '4':
			print 'Turn Right'
			turn_right()
		elif rec == '5':
			print 'Terminating Conection'
			conn.close()
			break
		else:
			print 'Unknown command = ' + rec
			
ser.close()
s.close()
