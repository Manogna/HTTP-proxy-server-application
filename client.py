'''
Subject : ACN (HTTP proxy server application)
Group : 12 
Reference from : https://github.com/MatthewFraser22/TCP-Proxy-Server-with-Multiprocessing

Created by @SaiManoj_Jonnalagadda 
Reviewed by : @Manogna_Sunkara 

'''
#importing required libraries
from socket import *
import sys

#server address destination
server_name = 'www.whynohttps.com'

#binding port number
serverPort = 80

print('Client is running...')
#creating a TCP socket - IPV4 is used
client_sock = socket(AF_INET,SOCK_STREAM)
#setting up connection from server to port
client_sock.connect((server_name,serverPort))
#send convert
convert = 'GET / HTTP/1.1\r\nHost:%s\r\n\r\n' % server_name
client_sock.send(convert.encode())
mod_convert = client_sock.recv(1024)
#output of the conversion
print('From server:',mod_convert.decode())
client_sock.close()
