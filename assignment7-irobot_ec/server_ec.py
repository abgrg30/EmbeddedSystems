##This Code is for Server for iRobot Control through BeagleBone in Python.
##Course: CSE291E ( Robotics/Embedded Systems)
##Assignment: 7 (Extra Credit)
##Last Modified: 22-Nov-2015
##Team: CodeIT
##Developers: Abhinav Garg; Abhijit Tripathi; Pulkit Bhatnagar
##University of California, San Diego

import Adafruit_BBIO.UART as UART 
import socket 
import serial 
import sys 
import math 
from time import sleep
 
Start = 128; 
SafeMode = 131; 
FullMode = 132; 
Drive = 137; 
DriveDirect = 145; 
WaitAngle = 157; 
Demo = 136; 
Sensors = 142; 
CoverandDock = 143; 
SensorStream = 148; 
QueryList = 149; 
StreamPause = 150; 
PlaySong = 141; 
Song = 140; 
BumpsandDrops = 7; 
Wall = 8; 
Distance = 19; 
Angle = 20; 
speed_left = 50; 
speed_right = 50; 
d = 0 
theta = 0 
theta2 = 0

#UART.setup("UART1")
HOST = '' # all available interfaces 
PORT = 5000 # TCP/IP port 
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
s.listen(10) #Start listening on socket 
print 'Socket now listening' 
conn, addr = s.accept() #wait to accept a connection - blocking call 
print 'Connected with ' + addr[0] + ':' + str(addr[1]) 

ser = serial.Serial(port='/dev/ttyO1', baudrate=57600, timeout=1.0) 
if ser < 0:
    print 'Server UART Creation Failed!!'
    sys.exit() 
else:
    print 'Server UART Created, fd = ' + str(ser)
    
ser.close() 
ser.open() 
if ser.isOpen():
    print 'Server Serial Ready' 
else:
    print 'Server Serial Closed??'
    sys.exit()
    
ser2 = serial.Serial(port='/dev/ttyO2', baudrate=57600, timeout=1.0) 
if ser2 < 0:
    print 'Server UART2 Creation Failed!!'
    sys.exit() 
else:
    print 'Server UART2 Created, fd = ' + str(ser2)
    
ser2.close()
ser2.open()
if ser2.isOpen():
    print 'Server Serial2 Ready'
else:
    print 'Server Serial2 Closed??'
    sys.exit() 

def recv_request():
    rec = conn.recv(100)
    if rec == '':
        print 'Server Receive Failed!!'
    else:
        print 'Server Data Received = ' + rec
    return rec
    
def serialread(rec):
    chunk = ser.read(100)
    if chunk == '':
        print 'Server UART read failed for :' + rec
    else:
        print 'Server UART data : ' + chunk
    return chunk


def initialize():
    ser.flush()
    ser2.flush()
    sleep(.1)
    ser.write(chr(Start))
    ser.write(chr(SafeMode))
    sleep(.1)
    #read_sensor('3')
    read_sensor('3')
    read_sensor('4')
    #read_sensor('4')
    
def stop():
    print 'Trying to stop.....'
    ser.write(chr(DriveDirect))
    ser.write(chr(0))
    ser.write(chr(0))
    ser.write(chr(0))
    ser.write(chr(0)) 

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
    theta2rad = (theta2 * 3.14 / 180)
    
    d = int( math.sqrt(math.pow((d+d2*math.cos(theta2rad)),2) + math.pow((d2*math.sin(theta2rad)),2)) )
    theta = theta + math.atanh( (d2*math.sin(theta2rad)) / (d+d2*math.cos(theta2rad)) )
    print d
    print theta 

def drive():
    ser.write(chr(DriveDirect))
    ser.write(chr((speed_right>>8)&0xFF))
    ser.write(chr(speed_right&0xFF))
    ser.write(chr((speed_left>>8)&0xFF))
    ser.write(chr(speed_left&0xFF))
    
def turn(dir,angle):
    global theta2
    sleep(0.1)
    
    if (dir == 'L' or dir == 'l'):
        ser.write(chr(Drive))
        ser.write(chr(0))
        ser.write(chr(100))
        ser.write(chr(0))
        ser.write(chr(1))
        angle = int(angle)
    elif (dir == 'R' or dir == 'r'):
        ser.write(chr(Drive))
        ser.write(chr(0))
        ser.write(chr(100))
        ser.write(chr(255))
        ser.write(chr(255))
        angle = ~(int(angle)) + 1
        
    ser.write(chr(WaitAngle))
    ser.write(chr((angle>>8)&0xFF))
    ser.write(chr(angle&0xFF))
    theta2=theta2+angle
    stop()
    sleep(0.1) 

def read_sensor(sense):
    #sleep(0.1)
    ser.write(chr(Sensors))
    if(sense == '1'): #Bump and Wheel
        ser.write(chr(BumpsandDrops)) ##7
        sleep(.1)
        s_data = ser.read(1)
    elif(sense == '2'): #Wall
        ser.write(chr(Wall)) ##8
        sleep(.1)
        s_data = ser.read(1)
    
    elif(sense == '3'): #Distance
        ser.write(chr(Distance)) ##19
        #sleep(.1)
        s_data = ser.read(2)
    elif(sense == '4'): #Angle
        ser.write(chr(Angle)) ##20
        #sleep(.1)
        s_data = ser.read(2)
    else:
        print 'Please select appropriate sensor'+str(sense)
    
    print 's_data'
    print s_data
    d = [ ord(c) for c in s_data ]
    print 'Sensor Data'
    print d
    return d
    
def GotoXY(x,y):
    # Assuming velocity 100mm/s calculate vel_Y and Y
    if(y<0):
        y = abs(y)
        yLow = ((~y)+1)&0xff;
        yHigh = (((~y)+1)>>8)&0xff;
        vHigh = 255;
        vLow = 156;
        print yLow
        print yHigh
    else:
        yLow = (y&0xff);
        yHigh = (y>>8)&0xff;
        vHigh = 0;
        vLow = 100;
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
        valx = 0;
        valy = 1;
    elif (x>0):
        angleH = 255;
        angleL = 166;
        valx = 255;
        valy = 255;
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
    print 'theta_home'
    print theta_home
    #d = ~d + 1
    dLow = (d&0xff)
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
    read_sensor('3')
    read_sensor('4')
    
    
 ##Added for Extra Credit avoid collision   
def neednewgoto(ch):
    stop()
    turn(ch, 90)
    drive()
    z=0
    while z<100:
    #ser.write(chr(156))
    #ser.write(chr(0))
    #ser.write(chr(100))
    #stop()
    	z = z + 2
    	sleep(0.2)
    return 100
        
def newgoto(x,y):
    
    #angle=0
    
    if x == '0':
        angle = 90
    else:
        #angle = int( math.atanh((int(y))/(int(x))) * 180 / 3.14)
        print 'y'
        print int(y)
        print 'x'
        print int(x)
	temp = int(y)/int(x)
	print 'temp'
	print temp
        angle = math.atan(temp)
	angle = math.degrees(angle)
        
    print 'angle'
    print angle
    
    if y < '0':
        ch = 'l'
    else:
        ch = 'r'
        
    distance = ( math.sqrt(math.pow(int(x),2) + math.pow(int(y),2)) )
    distance = int(distance)
    turn(ch,angle)
    drive()
    flag = '1'
    
    while distance>0:
        
	if flag == '1':
            ultra = ser2.read(1)
            print ultra

        if ultra == '1':
	    flag = '0'
            neednewgoto('r');
            neednewgoto('L');
            distance = distance-100
            neednewgoto('L');
            stop()
            turn('r', 90)
            ser2.flush()
	    drive()
        else:
            #l = read_sensor('3')
            #print 'read data'
            #print l
            dis = 10#l[0] * 256 + l[1]
            print 'distance left is'
            #print dis
            distance = distance - dis
	    print distance
    
    stop()
    
    
    
    
initialize() 
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
            read_sensor(sense)
            ser.flush()
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
        elif rec == '10':
            print 'New Goto XY'
            xCor = recv_request()
            yCor = recv_request()
            newgoto(xCor,yCor)
	elif rec == '11':
	    print ser2.read(1)
        else:
            print 'Unknown command = ' + rec
            
ser.close() 
s.close()
