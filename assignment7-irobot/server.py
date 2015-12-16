
##This Code is for Server for iRobot Control through BeagleBone in Python.
##Course: CSE291E ( Robotics/Embedded Systems)
##Assignment: 7
##Last Modified: 21-Nov-2015
##Team: CodeIT
##Developers: Abhinav Garg; Abhijit Tripathi; Pulkit Bhatnagar
##University of California, San Diego

import Adafruit_BBIO.UART as UART
import socket
import serial
import sys
import math
from time import sleep

##Definitions of iRobot Create OpenInterface Command Numbers
##See the Create OpenInterface manual for a complete list
 
 
##                Create Command              // Arguments
Start = 128;
SafeMode = 131;
FullMode = 132;
Drive = 137;                ## 4:   [Vel. Hi] [Vel Low] [Rad. Hi] [Rad. Low]
DriveDirect = 145;          ## 4:   [Right Hi] [Right Low] [Left Hi] [Left Low]
WaitAngle = 157;	    ## 2:    [Angle High] [Angle Low]
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
Wall = 8;
Distance = 19;
Angle = 20;

 
speed_left =  100;
speed_right = 100;

###############################################################
d = 0
theta = 0
theta2 = 0

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

def initialize():
	## Start Sequence

	ser.flush()

	ser.write(chr(Start))     ##128
	ser.write(chr(FullMode))  ##131
	sleep(.5)
	#read_sensor('3')
	#read_sensor('3')
	#read_sensor('4')
	#read_sensor('4')

	
def stop():
        #ser.flush()
	#initialize()
	##print 'Trying to stop.....'
        ser.write(chr(DriveDirect))
        ser.write(chr(0))
        ser.write(chr(0))
        ser.write(chr(0))
        ser.write(chr(0))
	#position()

def position():
	global d
	global theta
	global theta2

	d2_temp=read_sensor('3')
	print d2_temp
	if(d2_temp == []):
		d2_temp = [0,0]
	d2=d2_temp[0]*256+d2_temp[1]

	print d2

	print 'theta2'
	print theta2

	theta2rad = (theta2 * 3.14 / 180);
	
	d = int( math.sqrt(math.pow((d+d2*math.cos(theta2rad)),2) + math.pow((d2*math.sin(theta2rad)),2)) )
	theta = theta + math.atanh( (d2*math.sin(theta2rad)) / (d+d2*math.cos(theta2rad)) )
	#theta2=0

	print d
	print theta

def drive():

##stop
	#stop()
##forward
    	sleep(0.1)
	ser.write(chr(DriveDirect))
    	ser.write(chr((speed_right>>8)&0xFF))
    	ser.write(chr(speed_right&0xFF))
    	ser.write(chr((speed_left>>8)&0xFF))
    	ser.write(chr(speed_left&0xFF))
	        
	
def turn(dir,angle):
        #ser.flush()
	#initialize()
	#stop()

        global theta2

	sleep(0.1)
        if (dir == 'L' or dir == 'l'):
		ser.write(chr(Drive))	#move counter-clockwise at 100 mm/s
	        ser.write(chr(0))
        	ser.write(chr(100))
	        ser.write(chr(0))
        	ser.write(chr(1))

		angle = int(angle)
    		ser.write(chr(WaitAngle))
		ser.write(chr((angle>>8)&0xFF))
		ser.write(chr(angle&0xFF))
	
	elif (dir == 'R' or dir == 'r'):
                ser.write(chr(Drive))   #move clockwise at 100 mm/s
                ser.write(chr(0))
                ser.write(chr(100))
                ser.write(chr(255))
                ser.write(chr(255))
		
		angle = ~(int(angle)) + 1		#2's complement for -angle
                ser.write(chr(WaitAngle))
                ser.write(chr((angle>>8)&0xFF))
                ser.write(chr(angle&0xFF))
	theta2=theta2+angle
	stop()
	sleep(0.1)

def read_sensor(sense):
        ##initialize()
        #stop()
	sleep(0.1)
	##ser.write(chr(SensorStream))  ##148
        ##ser.write(chr(1))         ##1
        ser.write(chr(Sensors))
	#sleep(.5)

	if(sense == '1'): 		#Bump and Wheel
		ser.write(chr(BumpsandDrops)) ##7
        	sleep(.1)
		s_data = ser.read(1)	

	elif(sense == '2'):		#Wall
                ser.write(chr(Wall)) 	##8
                sleep(.1)
                s_data = ser.read(1)
	
	elif(sense == '3'):		#Distance
                ser.write(chr(Distance)) ##19
                sleep(.1)
                s_data = ser.read(2)

	elif(sense == '4'):		#Angle
                ser.write(chr(Angle)) 	##20
                sleep(.1)
                s_data = ser.read(2)
	else:
		print 'Please select appropriate sensor'+str(sense)
	
	print 's_data'+str(s_data)
	d = [ ord(c) for c in s_data ]
	print 'Sensor Data'
	print  d
	#ser.write(d)
	return d
	

def GotoXY(x,y):
	# Assuming velocity  100mm/s calculate vel_Y and Y
	if(y<0):
		y     = abs(y) 	
		yLow  = ((~y)+1)&0xff;
		yHigh = (((~y)+1)>>8)&0xff;
		vHigh = 255;
		vLow  = 156;
		print yLow
		print yHigh
	else:
		yLow  = (y&0xff);
		yHigh = (y>>8)&0xff;
		vHigh = 0; 
	        vLow  = 100;
	#Begin movement along Y axis
	ser.write(chr(137));
	ser.write(chr(vHigh));
	ser.write(chr(vLow));
	ser.write(chr(128));
	ser.write(chr(0));
	# Wait until travelling Y mm
	ser.write(chr(156));
	ser.write(chr(yHigh));	
	ser.write(chr(yLow));
	# Stop
	stop()	

	# Halt for 1 s
	sleep(1)
	
	# Rotate According to positive or negative X
	if(x<0):
		angleH = 0;
		angleL = 90;
		valx   = 0;
		valy   = 1;
	elif (x>0):   
		angleH = 255;
		angleL = 166;
		valx   = 255;
		valy   = 255;
	absXL = (abs(x))&0xFF;
	absXH = ((abs(x))>>8)&0xFF;
	# Write Data to rotate acc to x 
	if (x!=0):
		ser.write(chr(137));
		ser.write(chr(0));	
		ser.write(chr(100));
		ser.write(chr(valx));
		ser.write(chr(valy));
		# Rotate wait angle 90deg
		ser.write(chr(157));
		ser.write(chr(angleH));
		ser.write(chr(angleL));
		# Stop	
		stop();
		sleep(1);
		# Go along X now
		ser.write(chr(137));
		ser.write(chr(0));
		ser.write(chr(100));
		ser.write(chr(128));	
		ser.write(chr(0));	
	#Wait distance x
	##print 'Moving X'+chr(absXH)+chr(absXL)
		ser.write(chr(156));
		ser.write(chr(absXH));
		ser.write(chr(absXL));
		stop();		 			



def home():
	global d
	global theta
	global theta2

	theta = (theta * 180 / 3.14)
	print 'main angle'
	print theta
	print 'theta2'
	print theta2

	theta_home = (theta2 - theta)
	print theta_home

	#d = ~d + 1    
	print 'd='
	print d
	dLow  = (d&0xff)
        dHigh = (d>>8)&0xff

	print 'dhigh'
	print dHigh
	print 'dlow'
	print dLow

	turn('r',theta_home+180)

	ser.write(chr(137));
	ser.write(chr(0));
	ser.write(chr(100));
	ser.write(chr(128));
	ser.write(chr(0));

	ser.write(chr(156));
	ser.write(chr(dHigh));
	ser.write(chr(dLow));

	stop()
	d=0
	theta=0
	theta2=0

def reset_home():
        global d
        global theta
        global theta2


        d=0
        theta=0
        theta2=0
	

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


host = socket.gethostname();
print "host = "+host

try:
    s.bind((host, PORT)) #Bind socket to local host and port
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

s.listen(10)  #Start listening on socket
print 'Socket now listening'

conn, addr = s.accept()  #wait to accept a connection - blocking call
print 'Connected with ' + addr[0] + ':' + str(addr[1])

def send_request(cmd):
        sent = conn.send(cmd)
        if sent <= 0:
                print 'Server Send Failed!!'+str(cmd)

def recv_request():
        rec = conn.recv(100)

        if rec == '':
                print 'Server Receive Failed!!'
		#return 0
	else:
                print 'Server Data Received = ' + rec
		#return 1
	return rec



initialize()
#now keep talking with the client
while 1:
	#ser.flush()
	rec = recv_request()
	if(rec!=''):
		
		if rec == '1':
			print 'Drive Forward'
			drive()			

		elif rec == '2':
			print 'Turn R/L fixed (90deg)'
			turn_dir=recv_request()
			turn(turn_dir,90)
				
		elif rec == '3':
			print 'Turn R/L Programmable'
			turn_dir=recv_request()
			turn_angle=recv_request()
                        #print 'Turn_dir'+turn_dir
			#print 'Turn Angle'+turn_angle
			turn(turn_dir,turn_angle)

		elif rec == '4':
			print 'Read Sensor'
			sense = recv_request()
			msgRecv = read_sensor(sense)
			send_request(str(msgRecv));
			#ser.flush()

		elif rec == '5':
			print 'Goto XY'
			xCor = recv_request();
			yCor = recv_request();
			GotoXY(int(xCor),int(yCor));			

		elif rec == '6':
			print 'Home'
			home()
		elif rec == '7':
			print 'Reset Home'
			reset_home()
		elif rec == '8':
			print 'Terminating Conection'
			conn.close()
			break
		elif rec == '9':
			print 'Stop'
			stop()
			position()
		elif rec == '0':
			initialize()
		else:
			print 'Unknown command = ' + rec
			
ser.close()
s.close()
