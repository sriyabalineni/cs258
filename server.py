from collections import deque
from ctypes import sizeof
from pydoc import cli
import time
import sys
from xxlimited import new
# Import socket module
import socket    
import threading
import random
received_packets=deque([]) #dequeue for the received packets
packet_size=1 #setting packet size to 5
wrap_around=2**16

def sys_time(): #calculating the system time
    return int(round(time.time()*1000))

def sequence_check(current_packet): #checking if the packets are arriving in order
    #print(current_packet, type(current_packet))
    if len(received_packets)==0: #if the queue is empty, add the current packet
        received_packets.append(current_packet)
        return
    for i in range(len(received_packets)):
        if received_packets[i] > current_packet:
            received_packets.insert(i,current_packet)
            break
    i=0
    while i < len(received_packets)-1:
        if (received_packets[i]+packet_size)%wrap_around==received_packets[i+1]: #applying the wraparound
            received_packets.popleft()
        else:
            break

def checkIfDropped(): #randomized dropping of 1 packet for every 100 packets
    x=random.randint(1,100)
    if x==1:
        return False
    else:
        return True 

if __name__=="__main__":
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #initializing the socket
    print ("Socket successfully created")
    port=12340#reserving a port

    #10.251.239.58
    s.bind(('localhost' ,port))		
    print ("socket binded to %s" %(port))
    s.listen(5)	#put the socket into listening mode
    print ("socket is listening \n")		
    c,addr=s.accept() #connecting the the client
    print("Connection established with client %s" %(str(addr)))
    hello_msg=c.recv(1024) #receive message from the client
    print(hello_msg) #print the received message
    success_message="Success".encode('utf8')
    c.sendall(success_message) #send a success message
    no_of_packets_received=0
    no_of_packets_sent=0
    total_packets=0
    dropped=[]
    goodput_vals=[]

    #file1=open("seq_number_received.txt")
   

    #file2=open("seq_number_dropped.txt")
   
    #file3=open('goodput.txt')
   

    #file4=open('receiver_window.txt')
    
    while True:
    # Establish connection with client.	

        
        data=str(c.recv(1024).decode('utf8')).strip()
        #print('total received packets ', no_of_packets_received)
        for d in data.split(' '):
           # print(d,'received it now???')
           
            if checkIfDropped(): #first check if the packet has been dropped
                #print(d, 'type of d is ', type(d))
                #sequence_check(int(d)) #call the sequence order checking function
                #print(f'\nSequence number "{d}" received\n')
                #file1.write(str(d)+','+str(sys_time())+'\n') #writing the time at which the packet was received
                #file4.write(str(len(received_packets))+','+str(sys_time())+'\n') #writing the time at which the packet was received


                msg=(str(d)+' ').encode('utf8')
                c.sendall(msg)
                no_of_packets_received+=1 #increment the number of received packets
            else:
               
                #print('dropped')
                msg=(' ').encode('utf8')
                c.sendall(msg)
               # file2.write(str(d)+','+str(sys_time())+'\n')
            
            no_of_packets_sent+=1
            total_packets+=1
            
            if no_of_packets_received%1000==0: #calculating goodput after every 1000 packets received
               
               good_put=no_of_packets_received/no_of_packets_sent
               goodput_vals.append(good_put)
               print('Goodput------',good_put)
              # file3.write(str(no_of_packets_received)+"/"+str(no_of_packets_sent)+"="+str(no_of_packets_received/no_of_packets_sent)+"\n")

            if no_of_packets_received>=10000000: #stop the socket after 10 million packets
                print('total received packets ', no_of_packets_received)
                print('total sent packets ', no_of_packets_sent)
                print('avergae goodput = ', sum(goodput_vals)/len(goodput_vals))
                
                c.close()
                sys.exit(0)
