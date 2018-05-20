from socket import *

serverName = 'localhost'
serverPort = 12000
receiverIsReceiving = False
clientSocket = socket(AF_INET, SOCK_STREAM)
ACK = '0'
closingMessage = 'end trans'

def main():
    clientSocket.connect((serverName,serverPort)) 
    clientSocket.settimeout(2.0)
    receiverIsReceiving = True
    i = 0
    ACK = '0'
    sentence = raw_input("enter to start")

    while receiverIsReceiving:
        try:
            clientSocket.send(ACK)         #tell the server what the client is expecting
            recv = clientSocket.recv(1024)
            sequenceNumber = recv[-1:]
            print recv[:-1]

            if sequenceNumber == ACK:  #if the client got the packet it is expecting,
                if ACK == '0':
                    ACK = '1'
                else:
                    ACK = '0' #switch ACK which means the client is expecting the next packet

                i = i + 1
                if i > 5:
                    receiverIsReceiving = False #since there are 5 data items in the 'data' list
                    clientSocket.send(closingMessage)
                    clientSocket.close()

            elif sequenceNumber != ACK:  #if it gets the wrong packet, send the proper one, hence sending the ACK again
                clientSocket.send(ACK)
        except timeout:
            print 'timeout here'
            clientSocket.send(ACK)
            print ACK

if __name__ == '__main__':
    main()
