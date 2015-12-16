##This Code is for Client for iRobot Control through BeagleBone in Python.
##Course: CSE291E ( Robotics/Embedded Systems)
##Assignment: 7 (Extra Credit)
##Last Modified: 22-Nov-2015
##Team: CodeIT
##Developers: Abhinav Garg; Abhijit Tripathi; Pulkit Bhatnagar
##University of California, San Diego

import socket
import sys
 
HOST = '192.168.43.74'   # all available interfaces
PORT = 5000 # TCP/IP port
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def recv_request():
        rec = sock.recv(100)

        if rec == '':
                print 'Data from Server Failed!!'
                #return 0
        else:
                print 'Sensor Data = ' + rec
                #return 1
        return rec

def send_request(cmd):
	sent = sock.send(cmd)
        if sent <= 0:
	        print 'Client Send Failed!!'+str(cmd)



if sock < 0:
	print 'Client Socket Creation Failed!!'
else:
	print 'Client Socket Created, fd = ' + str(sock)
	host = socket.gethostname()
	print str(host)
	sock.connect((host,PORT))
	
	while 1:		
		print 'iROBOT CONTROL SYSTEM'
		print '1. Drive'
		print '2. Turn R/L fixed (90deg)'
		print '3. Turn R/L Programmable'
		print '4. Read Sensor'
		print '5. Goto X,Y'
		print '6. Return Home'
		print '7. Reset Home'
		print '8. Terminate Connection'
		print '9. Stop'
		print '10. Obstacle Avoidace'				## For Extra Credit
		cmd = raw_input('Please enter your choice:')
		
		send_request(cmd)
					
		if cmd == '2':
			turn_dir = raw_input('Enter the direction L/R:')
			send_request(turn_dir)
                elif cmd == '3':
                        turn_dir = raw_input('Enter the direction L/R:')
			send_request(turn_dir)
			turn_angle = raw_input('Enter the turn angle (0-360):')
			send_request(turn_angle)

		elif cmd == '4':
                        print '1. Bumps and Wheel Drops'
	                print '2. Wall'
        	        print '3. Distance'
                	print '4. Angle'
			sense = raw_input('Enter the Sensor to fetch data:')
                        send_request(sense)
			recv_request()
                        
		elif cmd == '5':
                       	x = raw_input('Enter the direction X (mm):')
                        send_request(x)
                        y = raw_input('Enter the Y (mm):')
                        send_request(y)
		
                elif cmd == '6':
                        print 'Returning Home...'

                elif cmd == '7':
                        print 'This is my new Home...'

		elif cmd == '8':
			print 'Terminating Code'
			break;

                elif cmd == '9':
                        print 'Stopping'

                elif cmd == '10':
                        x = raw_input('Enter the direction X (mm):')
                        send_request(x)
                        y = raw_input('Enter the direction Y (mm):')
                        send_request(y)

		else:
			continue
		
	sock.close()
