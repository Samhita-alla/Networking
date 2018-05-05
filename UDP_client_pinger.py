import time
from socket import *
clientsocket = socket(AF_INET6,SOCK_DGRAM)
server_socket_addr = ('localhost',12000)
clientsocket.settimeout(1)
try:
	for i in range(1,11):
		start = time.time()
		message = 'Ping #' + str(i) + " " + time.ctime(start)
		try:
			s = clientsocket.sendto(message,server_socket_addr)
			print 'Sent: ',message
			msg, serveraddr = clientsocket.recvfrom(2048)
			print 'Received: ',msg
			end = time.time()
			elapsed = end-start
			print "RTT: " + str(elapsed) + " seconds\n"
		except timeout:
			print '#'+str(i)+' Requested timeout\n'
finally:
	print 'closing socket'
	clientsocket.close()
