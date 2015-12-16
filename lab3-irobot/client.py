##This Code is for Server for iRobot Control through BeagleBone in Python.
##Course: CSE291E ( Robotics/Embedded Systems)
##Lab: 3
##Last Modified: 210Nov-2015
##Team: CodeIT
##Developers: Abhinav Garg; Abhijit Tripathi; Pulkit Bhatnagar
##University of California, San Diego

import socket
import sys
 
HOST = 'localhost'   # all available interfaces
PORT = 5000 # TCP/IP port
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if sock < 0:
	print 'Client Socket Creation Failed!!'
else:
	print 'Client Socket Created, fd = ' + str(sock)
	host = socket.gethostname()
	print str(host)
	sock.connect((host,PORT))
	
	while 1:		
		print 'iROBOT CONTROL SYSTEM'
		print '1. Move Forward'
		print '2. Stop'
		print '3. Turn Left'
		print '4. Turn Right'
		print '5. Terminate Connection'
		cmd = raw_input('Please enter your choice:')
		
		sent = sock.send(cmd)
		
		if sent <= 0:
			print 'Client Send Failed!!'
			
		if cmd == '5':
			print 'Terminating'
			break;
		else:
			continue
		
	sock.close()
