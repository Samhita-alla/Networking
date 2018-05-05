import random
from socket import *
serversocket = socket(AF_INET6,SOCK_DGRAM)
serversocket.bind(('',12000))
print 'Started UDP Server'
while True:
	rand = random.randint(0,10)
	msg, clientaddr = serversocket.recvfrom(2048)
	msg = msg.upper()
	if rand<4:
		continue
	serversocket.sendto(msg,clientaddr)