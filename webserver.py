#localhost:5000/hey_webserver.html
from socket import *
serversocket = socket(AF_INET, SOCK_STREAM)
serverport = 5000
serversocket.bind(('',serverport))
serversocket.listen(1)
print 'Server'
while True:
	connectedsocket, addr = serversocket.accept()
	try:
		msg = connectedsocket.recv(2048)
		print msg
		print
		#print msg.split()[0]
		filename = msg.split()[1]
		print filename
		print
		f = open(filename[1:])
		outputdata = f.read()
		print outputdata
		print
		connectedsocket.send('\n')
		connectedsocket.send('HTTP/1.1 200 OK\n')
		connectedsocket.send('Connection: close\n')
		string_len = 'Content-length: '+str(len(outputdata))+'\n'
		connectedsocket.send(string_len)
		connectedsocket.send('Content-Type: text/html\n')
		connectedsocket.send('\n')
		connectedsocket.send('\n')
		for i in outputdata:
			connectedsocket.send(i)
		connectedsocket.close()
	except IOError:
		print 'IOError'
		connectedsocket.send('HTTP/1.1 404 Not Found\r\n')
		connectedsocket.send('Content-Type: text/html\r\n\r\n')
		connectedsocket.send('<html><head></head><body><h1>404 Not Found</h1></body></html>')
		connectedsocket.close()

