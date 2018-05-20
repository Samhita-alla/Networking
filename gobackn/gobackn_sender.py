# sender.py - The sender in the reliable data transfer protocol
#These aren't like client and server but instead both act like servers and they run on UDP protocol
#python 3
import packet
import socket
import sys
import _thread
import time
import udt

from timer import Timer

PACKET_SIZE = 512 #each packet is of 512 bytes
RECEIVER_ADDR = ('localhost', 8080)
SENDER_ADDR = ('localhost', 12000)
SLEEP_INTERVAL = 0.05
TIMEOUT_INTERVAL = 0.5
WINDOW_SIZE = 4

# Shared resources across threads
base = 0
mutex = _thread.allocate_lock()#mutex lock
send_timer = Timer(TIMEOUT_INTERVAL)

# Sets the window size
def set_window_size(num_packets):
    global base
    return min(WINDOW_SIZE, num_packets - base)

# Send thread
def send(sock, filename):
    global mutex #global variables
    global base
    global send_timer

    # Open the file
    try:
        file = open(filename, 'r')#read mode
    except IOError:
        print('Unable to open', filename)
        return
    #file.write('hey')
    # Add all the packets to the buffer
    packets = []#packets list wherein we store all the packets of size 512 bytes
    seq_num = 0
    while True:
        data = file.read(PACKET_SIZE)
        #print data
        if not data:
            #print 'yes'
            break
        packets.append(packet.make(seq_num, data))#packet.py file and all the packets are being appended to the packets list 
        seq_num += 1

    num_packets = len(packets)
    print('I gots', num_packets)
    window_size = set_window_size(num_packets)
    next_to_send = 0
    base = 0

    # Start the receiver thread
    _thread.start_new_thread(receive, (sock,))#this thread automatically calls the receive function when the receiver sends an ACK to the sender

    while base < num_packets:
        mutex.acquire()#acquire lock
        # Send all the packets in the window
        while next_to_send < base + window_size:#here the first 4 packets won't be sent at the same time because there are chances that during the traversal of the packets from the sender to the receiver, 
        #sender might receive an ACK packet which immediately invokes receive() method because of the thread we created 
            print('Sending packet', next_to_send)
            udt.send(packets[next_to_send], sock, RECEIVER_ADDR)
            next_to_send += 1

        # Start the timer
        if not send_timer.running():
            print('Starting timer')
            send_timer.start()

        # Wait until a timer goes off or we get an ACK
        while send_timer.running() and not send_timer.timeout():
            mutex.release()
            print('Sleeping')
            time.sleep(SLEEP_INTERVAL)
            mutex.acquire()

        if send_timer.timeout():
            # Looks like we timed out
            print('Timeout')
            send_timer.stop();
            next_to_send = base
        else:
            print('Shifting window')#shifts after the window ends(after 4 packets are sent)
            window_size = set_window_size(num_packets)
        mutex.release()

    # Send empty packet as sentinel
    udt.send(packet.make_empty(), sock, RECEIVER_ADDR)
    file.close()
    
# Receive thread
def receive(sock):
    global mutex
    global base
    global send_timer

    while True:
        pkt, _ = udt.recv(sock);
        ack, _ = packet.extract(pkt);

        # If we get an ACK for the first in-flight packet
        print('Got ACK', ack)
        if (ack >= base):
            mutex.acquire()
            base = ack + 1#this is the basis for go-back-n because packets which encounter time-out are sent from the number where ACK's haven't yet been received
            print('Base updated', base)
            send_timer.stop()
            mutex.release()

# Main function
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Expected filename as command line argument')
        exit()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)
    filename = sys.argv[1]#provide a file as command line argument(b.txt) which has content in it

    send(sock, filename)
    sock.close()