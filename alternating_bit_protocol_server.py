#stop and wait protocol
from socket import *

serverPort = 12000
closingMessage = 'end trans'
receivng = False

data = ['Harry','You','Are','The','Chosen','One']

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print 'READY TO WORK'

    while True:
        connectionSocket, addr = serverSocket.accept()
        receiving = True
        sequenceNumber = '0'
        nextPacketToSend = 0
        while receiving == True:
            ACK = connectionSocket.recv( 1024 )
            print ACK
            if ACK == sequenceNumber: #if the client is expecting the data which the server is willing to send
                connectionSocket.send( data[nextPacketToSend] + sequenceNumber )

                if sequenceNumber == '0':
                    sequenceNumber = '1'
                else:
                    sequenceNumber = '0'

                nextPacketToSend = nextPacketToSend + 1

            elif ACK != sequenceNumber: #if it is expecting something else
                nextPacketToSend = nextPacketToSend - 1

                if sequenceNumber == '0':
                    sequenceNumber = '1'
                else:
                    sequenceNumber = '0'

                connectionSocket.send( data[nextPacketToSend] + ' ' + sequenceNumber )

            if ACK == closingMessage:
                connectionSocket.close()
                receiving = False

if __name__ == '__main__':
    main()