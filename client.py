
import socket
import random
import json
from collections import deque


# Define the maximum sequence number and the window size
max_seq_num = 2**16

# Create a TCP/IP socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the IP address and port number of the server
server_address = ('localhost' , 12340)

# Connect to the server
client_socket.connect(server_address)

# Send the initial string to the server
initial_string = "network"
client_socket.sendall(initial_string.encode())

# Receive the connection setup success message from the server
data = client_socket.recv(1024)
success_message = data.decode()
print("Received success message from server: ", success_message)


#function to generate the system time
def sys_time():
    return int(round(time.time()* 1000))

import time
window_size=2
seq_counter=0 #the sequence numbers that we are sening to the server
client_window=deque([])
extra_ack=[]

dropped_packets=[]



def processAck(sock): #function for processing the acknowledgement
    data=str(sock.recv(1024).decode('utf8')).strip() #receive acknowledgement from the server
    #print('data in processack', data)
    #print('extra acks is ', extra_ack)
    if data is not None and data != "":
        #print(data,'SAY WHAT NOW')
        for d in data.split(' '):
            #print(int(d), 'ack received')

            if len(client_window)>0 and int(d) == client_window[0][0]: #check if the acknowledgement received is for the sent packet
                client_window.popleft()
                while len(client_window)!=0 and client_window[0][0] in extra_ack:
                    extra_ack.remove(client_window[0][0])
                    client_window.popleft()
            else:
                extra_ack.append(int(d))
                
                
                retransmit(sock)

          
        
        window_resize(sock) #change window size
        #print('window size is ', window_size)
        #print('-----------------------------------------------')
    else:
        print('entered else DROPPEDDDD')    
       # print('-----------------------------------------------')
       
            
window_increment=0

def retransmit(sock):
    global window_size
    global window_increment
    i = 0
    
    if len(extra_ack)>=100: #checking for 20 out of order packets
        if len(client_window)>0:
            msg=(str(client_window[i][0])+' ').encode('utf8')
            sock.sendall(msg)
            window_size=int(window_size/2) #divide the window size by half
            
            window_increment=1
            client_window[i][1] = sys_time() #update the time to the current time
            processAck(sock)
           

def window_resize(sock):
    global window_increment
    maxsize=1000000
    global window_size
    temp = window_size
    if window_increment==0:
        new_window_size=window_size*2 #doubling the window size if the acknowledgment is in order
    else:
        new_window_size=window_size+1 #else incrementing it by 1
    
    if new_window_size>=maxsize:
        window_size=maxsize
    elif new_window_size<=0:
        window_size=1
    else:
        window_size=new_window_size
    if len(client_window)> window_size:
        window_size=window_size*2
    file1.write(str(window_size)+","+str(sys_time())+"\n")

    #print('new window size is ',window_size)

file1 = open("windowsize.txt", 'a')  # append mode
file1.write(str(window_size)+","+str(sys_time())+"\n") 
while 1:
        print('len of window_size and client size are ', window_size, len(client_window))
        if len( client_window) < window_size:
            #print('what the fuck', client_window)
            client_window.append([seq_counter, sys_time()]) #add the sequence number and the time at which it was sent
            temp=str(seq_counter)+' '
            msg=temp.encode('utf8')
            client_socket.sendall(msg) #send it to the server
            seq_counter=(seq_counter+1)%max_seq_num #wraparound after 2^16 packets
            #print(client_window, 'before sending to server')
            processAck(client_socket)
            #print('processing done', client_window, window_size)
        #else:
            #window_size=window_size*2






