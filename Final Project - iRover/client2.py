import socket
import sys
from time import sleep

#HOST = '192.168.43.2'   # all available interfaces
HOST = '192.168.43.2'  # all available interfaces
PORT = 5000 # TCP/IP port
 

flag = True;

angle = 0;

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if sock < 0:
	print 'Client Socket Creation Failed!!'
else:
	print 'Client Socket Created, fd = ' + str(sock)
	host = socket.gethostname()
	print str(host)
	sock.connect((HOST,PORT))
	f = open('camdata.txt', 'r')
	
	if f < 0:
		print 'File Open Failure'
	else:
		cnt = 0
		while 1:		
			print 'RADAR CONTROL SYSTEM'
			print '12. Search Object'
			print '13. Send Angle'
			print '14. Object Detection'
			print '10. Terminate Connection'
			cmd = raw_input('Please enter your choice:')

			if cmd == '12':
				sent = sock.send(cmd)
                		if sent <= 0:
                        		print 'Client Send Failed!!'
				while 1:
          				if (sock.recv(1) == 'g'):
					  	var = f.readline()
					  	print var
					  	if var == 'q\n':
							#sock.send(var)
							break
						elif var == '' or var == '\n':
							sock.send('n\n')
							continue
						#elif var != 'n\n':
							#if cnt == 0:
							#	cnt = cnt + 1
							#elif cnt >= 20:
							#	cnt = 0
							#	var = 'n\n'
							#else:
							#	cnt = cnt + 1
							#	var = 'n\n'
							#sock.send(var+'')
					  	else:
						  	sock.send(var+'')
				  	else:
            					f.flush()
				sock.send('10')
				f.close()
				break	
		
			elif cmd == '13':
				sent = sock.send(cmd)
                		if sent <= 0:
                        		print 'Client Send Failed!!'
				while 1:
					var = f.readline()
					print var
					if var == 'q' or var == '':
						break
					else:
						if flag==True:
							global angle;
							angle = var;
							flag = False	
						#sock.send(var+'')
						sock.send(angle+'')
					sleep(0.1)
				sock.send('10')
				f.close()
				break

			elif cmd == '15':
				sent = sock.send(cmd)
				if sent <=0:
					print 'Client Send Failed!!'
								
				

			elif cmd == '10':
				sent = sock.send(cmd)
				break
			else:
				print 'Unknown Command!!'
					
	sock.close()
