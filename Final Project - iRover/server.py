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

last_cmd = 0
prevdistance = '100'

#UART.setup("UART1")
HOST = ''   # all available interfaces
PORT = 5000 # TCP/IP port


ser_mbed = serial.Serial(port='/dev/ttyO1', baudrate=9600, timeout=0.1)#, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)
ser = serial.Serial(port='/dev/ttyO2', baudrate=57600, timeout=0.1)#, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)

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

if ser_mbed < 0:
	print 'Server UART Creation Failed!!'
else:
	print 'Server UART Created, fd = ' + str(ser_mbed)
	
ser_mbed.close()
ser_mbed.open()

if ser_mbed.isOpen():
        print 'MBED Server Serial Ready'
else:
        print 'MBED Server Serial Closed??'

def initialize():
	## Start Sequence
	ser.flush()
	ser.write(chr(Start))     ##128
	ser.write(chr(FullMode))  ##131
	sleep(.5)

	
def stop():
        ser.write(chr(DriveDirect))
        ser.write(chr(0))
        ser.write(chr(0))
        ser.write(chr(0))
        ser.write(chr(0))


def forward():
##forward
##    	sleep(0.1)
##	ser.write(chr(DriveDirect))
##    	ser.write(chr((speed_right>>8)&0xFF))
##    	ser.write(chr(speed_right&0xFF))
##    	ser.write(chr((speed_left>>8)&0xFF))
##    	ser.write(chr(speed_left&0xFF))

	ser.write(chr(Drive))	#move at 100 mm/s
	ser.write(chr(0))
        ser.write(chr(50))
	ser.write(chr(128))
        ser.write(chr(0))
	##stop()        
	

def reverse():
##reverse
	ser.write(chr(Drive))	#move at -100 mm/s
	ser.write(chr(255))
        ser.write(chr(128))
	ser.write(chr(128))
        ser.write(chr(0))
	#stop()

def turn_left():
	ser.write(chr(Drive))	#move counter-clockwise at 100 mm/s
	ser.write(chr(0))
        ser.write(chr(40))
	ser.write(chr(0))
        ser.write(chr(1))
	#stop()

def waitangle_left(theta):
	stop()
	ser.write(chr(Drive))	#move counter-clockwise at 100 mm/s
	ser.write(chr(0))
        ser.write(chr(40))
        ser.write(chr(0))
       	ser.write(chr(1))

	ser.write(chr(WaitAngle))
	ser.write(chr((theta>>8)&0xFF))
	ser.write(chr(theta&0xFF))
	stop()

def turn_right():               
	ser.write(chr(Drive))   #move clockwise at 100 mm/s
        ser.write(chr(0))
        ser.write(chr(40))
        ser.write(chr(255))
        ser.write(chr(255))
	#stop()

def waitangle_right(theta):
	stop()
        ser.write(chr(Drive))   #move clockwise at 100 mm/s
        ser.write(chr(0))
        ser.write(chr(40))
        ser.write(chr(255))
        ser.write(chr(255))
	
        ser.write(chr(WaitAngle))
        ser.write(chr((theta>>8)&0xFF))
        ser.write(chr(theta&0xFF))
	stop()

def rev_horn():               
	ser.write(chr(Song))   #move clockwise at 100 mm/s
        ser.write(chr(0))
        ser.write(chr(1))
        ser.write(chr(91))
        ser.write(chr(10))
	ser.write(chr(PlaySong))   #move clockwise at 100 mm/s
        ser.write(chr(0))
	
def obstacle_detect():
	#ser_mbed.flushInput()
	#ser_mbed.flushOutput()
	global prevdistance

	ser_mbed.write("2".encode())
	distance = ser_mbed.readline()

	if distance == '' or distance == '0\n' or distance == '\n':
		print 'prev distance used:'+prevdistance
		distance = prevdistance
		ser_mbed.flushInput()
	else:
		prevdistance = distance
		print prevdistance

	print 'In function obstacle detect, distance='+distance
	return int(distance)

def position():
	#ser_mbed.flushInput()
	#ser_mbed.flushOutput()
	ser_mbed.write("3".encode())
	coordinate = ser_mbed.read(30)
	print 'In function Position, gps='+coordinate
	return coordinate

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
    s.bind((HOST, PORT)) #Bind socket to local host and port
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

def camcontrol():
	rec = recv_request()
	if rec == '10':
		stop()
		conn.close()
		return 0
	elif rec == '' or rec == '\n' or rec == '\r\n':
		return 0
		
	else:
		if int(rec)>0:
			turn_right()
			sleep(0.1)
			stop()
		else:         
			turn_left()
			sleep(0.1)
			stop()
	return 1
 
def anglecontrol(var):
	if var != '\n' and var != '' and var != 'n\n':
    		#print 'degree:'+var
    		j = int(var)
    		#print 'int degree:'+str(j)
    		if j < 0:
      			waitangle_right(j)
			#turn_right()
    		else:
      			waitangle_left(j)
			#turn_left()
		#sleep(0.1)
		#stop()
		return 1
	else:
   		return 0
 
 
uflag = 0
def ultracheck(lrcount):
	global uflag
	if uflag == 0:
		ser_mbed.write("1".encode())
		sleep(0.01)
                lrcount = lrcount - 1
		if lrcount < -10:
			uflag = 1
        else:
                ser_mbed.write("0".encode())
		sleep(0.01)
                lrcount = lrcount + 1
		if lrcount > 15:
			uflag = 0
	return lrcount

def recoverultra(count):
	global uflag
	uflag = 0
	while count < 0:
		ser_mbed.write("0".encode())
		sleep(0.01)
		count = count + 1
	while count > 0:
		ser_mbed.write("1".encode())
		sleep(0.01)
		count = count - 1	
	return count	

initialize()
#now keep talking with the client
while 1:
	rec = recv_request()
	if(rec!=''):
		
		if rec == '1' or rec == '1\r\n':
			if(last_cmd != rec):
				print 'Drive Forward'
				forward()
				last_cmd=rec
			else:
				print 'stop'
				stop()
				last_cmd=0
		elif rec == '2' or rec == '2\r\n':
			if(last_cmd != rec):
				print 'Reverse'
				reverse()
				rev_horn()
				last_cmd=rec
			else:
				print 'stop'
				stop()
				last_cmd=0
				
		elif rec == '3' or rec == '3\r\n':
			if(last_cmd != rec):
				print 'Turn Right'
				turn_right()
				last_cmd=rec
			else:
				print 'stop'
				stop()
				last_cmd=0

		elif rec == '4' or rec == '4\r\n':
			if(last_cmd != rec):
				print 'Turn Left'
				turn_left()
				last_cmd=rec
			else:
				print 'stop'
				stop()
				last_cmd=0

		elif rec == '5' or rec == '5\r\n':
			print 'Look Left'
			ser_mbed.write("1".encode())
			rev_horn()
			stop()
				
	
		elif rec == '6' or rec == '6\r\n':
			print 'Look Right'
			ser_mbed.write("0".encode())
			rev_horn()
			stop()
			
		elif rec == '7' or rec == '7\r\n':
			print 'Obstacle @:'
			stop()
			dis = obstacle_detect()
			print dis
			send_request(str(dis)+'\n')

		elif rec == '8' or rec == '8\r\n':
			print 'GPS'
			stop()
			gps = position()
			print gps
			send_request(gps+"")

		elif rec == '9' or rec == '9\r\n':
			stop()
			
		elif rec == '10' or rec == '10\r\n':
			print 'Terminating Conection'
			stop()
			conn.close()
			break
##Hidden Commands

		elif rec == '0' or rec == '0\r\n':
			initialize()
            
		elif rec == '11' or rec == '11\r\n':
			turns = 20
			lrcount = 0
			mainflag = 0

			while turns > 0:
				forward()
				check = obstacle_detect()
				maxlr = 80
                        	while check > 50:
                           		check = obstacle_detect()
					lrcount = ultracheck(lrcount)
                        	stop()
				#lrcount = recoverultra(lrcount)
				if mainflag == 0:
                        		turn_left()
				else:
					turn_right()
                        	max = 25
                        	count = 0
				check = obstacle_detect()
                        	while (check < maxlr) and (count <= max):
					if mainflag == 0:
                           			count = count + 1
						#ser_mbed.write("0".encode())
						#lrcount = lrcount + 1
						check = obstacle_detect()
					else:
						count = count - 1
						#ser_mbed.write("1".encode())
						#lrcount = lrcount - 1
						check = obstacle_detect()
                        	stop()
				rev_horn()
            
                        	if count >= max:
					if mainflag == 0:
						mainflag = 1
                           			turn_right()
						check = obstacle_detect()
                           			while check < maxlr:
							#ser_mbed.write("1".encode())
							#lrcount = lrcount - 1
                           				check = obstacle_detect()
					else:
						mainflag = 0
						turn_left()
						check = obstacle_detect()
						while check < maxlr:
							#ser_mbed.write("0".encode())
							#lrcount = lrcount + 1
							check = obstacle_detect()
                           		stop()
                           		rev_horn()
				turns = turns - 1
				recoverultra(lrcount)

		elif rec == '12':
			turns = 20
			lrcount = 0
			mainflag = 0
			var = 'n\n'
			aflag = 0
			maxlr = 100
			maxdis = 50

			while turns > 0:
				forward()
				check = obstacle_detect()
				var = 'n\n'

				if aflag == 1:
					aflag = 0
					if maxdis > 25:
						maxdis = 25
					else:
						if check <= maxdis:
							print 'object found'
							stop()
							rev_horn()
							break
				else:
					maxdis = 50	

                        	while check > maxdis and var == 'n\n':
					send_request('g')
					var = recv_request()
                           		check = obstacle_detect()
					#lrcount = ultracheck(lrcount)
                        	stop()
				#lrcount = recoverultra(lrcount)
				if (anglecontrol(var) == 1):
					aflag = 1
					continue
				else:
					aflag = 0

				if mainflag == 0:
                        		turn_left()
				else:
					turn_right()
                        	max = 30
                        	count = 0
				var = 'n\n'
				check = obstacle_detect()
                        	while (check < maxlr) and (count <= max) and (var == 'n\n'):
					send_request('g')
					var = recv_request()
					if mainflag == 0:
                           			count = count + 1
						#ser_mbed.write("0".encode())
						#lrcount = lrcount + 1
						check = obstacle_detect()
					else:
						count = count - 1
						#ser_mbed.write("1".encode())
						#lrcount = lrcount - 1
						check = obstacle_detect()
                        	stop()
				rev_horn()
            
                        	if count >= max:
					if mainflag == 0:
						mainflag = 1
                           			turn_right()
						var = 'n\n'
						check = obstacle_detect()
                           			while check < maxlr and var == 'n\n':
							#ser_mbed.write("1".encode())
							#lrcount = lrcount - 1
                           				check = obstacle_detect()
					else:
						mainflag = 0
						turn_left()
						var = 'n\n'
						check = obstacle_detect()
						while check < maxlr and var == 'n\n':
							#ser_mbed.write("0".encode())
							#lrcount = lrcount + 1
							check = obstacle_detect()
                           		stop()
                           		rev_horn()

 
                                if (anglecontrol(var) == 1):
                                        aflag = 1
                                else:
                                        aflag = 0

				turns = turns - 1
			#lrcount = recoverultra(lrcount)
		elif rec == '13':
			get = 0
			while 1:
				forward()
				get = obstacle_detect()
				
				if get == '' or get == '\n':
					get = 40
				if get < 30:
					stop()
					rev_horn()
					break

				rec = recv_request()

				if rec == 'q\n':
					stop()
					conn.close()
					break
				elif rec == '' or rec == '\n' or rec == '\r\n' or rec == 'n\n':
					continue
				else:
					if int(rec)>0:
						#turn_right()
						#sleep(0.1)
						waitangle_right(int(rec))
						stop()
					else:         
						#turn_left()
						#sleep(0.1)
						waitangle_left(int(rec))
						stop()
			break  
		elif rec == '14':
			forward()
			check = obstacle_detect()  
			while check > 50:
				check = obstacle_detect()
			stop()
					
		else:
			print 'Unknown command = ' + rec
			
ser.close()
s.close()

