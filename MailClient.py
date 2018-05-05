#allow less secure apps
import ssl
import getpass
import base64 #base64 encoding technique
from socket import *

helloCommand = 'HELO localhost\r\n'
endmsg = "\r\n.\r\n"
mailserver = 'smtp.gmail.com'
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket = ssl.wrap_socket(clientSocket, #we are creating a secure socket using either ssl or tls     
                ssl_version=ssl.PROTOCOL_SSLv23,     
                ciphers="HIGH:-aNULL:-eNULL:-PSK:RC4-SHA:RC4-MD5",
                cert_reqs=ssl.CERT_REQUIRED)

clientSocket.connect((mailserver, 465))
recvconnect = clientSocket.recv(1024)
print recvconnect

if recvconnect[:3] != '220':
	print '220 reply not received from server.'

#Send hellocommand and print server response
print "Hello Server!"
clientSocket.send(helloCommand)
recvhelo = clientSocket.recv(1024)
print recvhelo
if recvhelo[:3] != '250':
	print '250 reply not received from server.'

#sending email ID and password
Email=raw_input("Insert Email: ")
Password= getpass.getpass(prompt='Insert Password: ')


UP=("\000"+Email+"\000"+Password).encode("base64")
#print UP
UP=UP.strip("\n")
login = 'AUTH PLAIN '+ UP + '\r\n'
print login
clientSocket.send(login)
recv_from_SSL = clientSocket.recv(1024)
print recv_from_SSL



#Send MAIL FROM command and print server response.
print "Sending MAIL FROM Command"
clientSocket.send('MAIL FROM: <'+ Email+'>\r\n')
recv2 = clientSocket.recv(1024)
print recv2
if recv2[:3] != '250':
	print '250 reply not received from server.'

#Send RCPT TO command and print server response.
print "Sending RCPT TO Command"
receiver =raw_input("Send email to: ")
toCommand = 'RCPT TO: <'+ receiver +'>\r\n'
clientSocket.send(toCommand)
recv2 = clientSocket.recv(1024)
print recv2
if recv2[:3] != '250':
	print '250 reply not received from server.'

#Send DATA command and print server response.
dataCommand = 'DATA\r\n'
print dataCommand
clientSocket.send(dataCommand)
recv4 = clientSocket.recv(1024)
print recv4
Subject=raw_input("Subject: ")
Text=raw_input("Message: ")
clientSocket.send("Subject: "+Subject+"\r\n"+Text+"\r\n"+ endmsg +"\r\n")
recv5 = clientSocket.recv(1024)
print recv5

#quit
clientSocket.send("QUIT\r\n")
recv6 = clientSocket.recv(1024)
print recv6
clientSocket.close()
