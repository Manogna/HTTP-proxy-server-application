'''
Subject : ACN (HTTP proxy server application)
Group : 12 
Description : Python socket programming is used, as well as the HTTP protocol. 
The goal of this project was to create a network application that used the stream socket API. 
Simple HTTP GET requests are understood by this programme.
Reference from : https://github.com/MatthewFraser22/TCP-Proxy-Server-with-Multiprocessing

Created by @Manogna_Sunkara 
Reviewed by : @SaiManoj_Jonnalagadda 

'''
#importing required libraries
from socket import *
import sys
import os
import multiprocessing

def function(client_sock, adr, msg):
    # Extracting the filename
    # file_name = msg.split()[1].partition("/")[2]
    if "Referer" in msg:
        client_sock.close()
        return
    # print(msg)

    try:
        file_name = msg.split()[1].replace("/", "")
    except Exception:
        print("Cannot extract request.")
        client_sock.close()
        return
    # print(file_name)
    file_status = "false"
    file_to_use = "./cache/" + file_name
    # print(file_to_use)
    try:
        print("Checking to see if file exists...")
        f = open(file_to_use, "rb")
        outputdata = f.readlines()
        file_status = "true"
        
        buf = b''
        for i in range(len(outputdata)):
            buf = buf + (outputdata[i])

        client_sock.sendall(buf)
        print('Read from cache!')
        
    # To do the error_handling for file not in cache
    except IOError:
        if file_status == "false":

            # Proxy server proxy creation
            c = socket(AF_INET, SOCK_STREAM)

            hostn = file_name.replace("www.","",1)
            if "Referer" not in msg:
                try:
                    # For missing objects from client
                    
                    request = "GET / HTTP/1.1\nHost: "+file_name+"\n\n"
                    request = request.encode()
                    
                    c.connect((file_name, 80))  
                    print("Request to " + file_name + " is made.")
                    c.sendall(request)  
                    
                    buffer = receive_all(c)
                    print("Response from " + file_name + " is recieved:")
                    print(buffer)
                    print('\n')
                    status_code = int(buffer.decode().split()[1])

                    client_sock.sendall(buffer)
                    if (status_code == 200):
                        tmpFile = open("./cache/" + file_name,"wb")
                        tmpFile.write(buffer)
                        tmpFile.close()
                    else:
                        http_error_handle(status_code, client_sock)
                except error as e :  
                    print(e)
                    print("Request not valid")
                    request = "HTTP/1.1 400 Bad Request \r\n\r\n"
                    client_sock.sendall(request.encode())
            else:
                print("Attempting to redirect.")
        else:
            # Output (HTTP error message) for page not found
            client_sock.send("HTTP/1.0 404 sendErrorErrorError\r\n")
            client_sock.send("Content-Type:text/html\r\n")
            client_sock.send("\r\n")
            # close method to close the clients
            c.close()
            
    client_sock.close()

#Recieve functions
def receive_all(sock):
    buf = b''
    while True:
        line = sock.recv(512)
        buf += line
        if len(line) < 512:
            break
    return buf

#Function for error handling
def http_error_handle(status, sock):
    if (status == 301):
        request = "HTTP/1.1 301 Moved Permanently \r\n\r\n"
        request = request.encode()
        sock.sendall(request) 
    elif(status == 302):
        request = "HTTP/1.1 302 Found \r\n\r\n"
        request = request.encode()
        sock.sendall(request) 
    elif(status == 400):
        request = "HTTP/1.1 Bad Request \r\n\r\n"
        request = request.encode()
        sock.sendall(request) 
    elif(status == 404):
        request = "HTTP/1.1 404 Not Found \r\n\r\n"
        request = request.encode()
        sock.sendall(request) 
    elif(status == 500):
        request = "HTTP/1.1 500 Internal Server Error \r\n\r\n"
        request = request.encode()
        sock.sendall(request) 
    else:
        request = "HTTP/1.1 Bad Request \r\n\r\n"
        request = request.encode()
        sock.sendall(request) 


def cache_folder():
    if not (os.path.exists("./cache")):
        os.mkdir("./cache")
        print("Creating cache folder is successful!")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Usage : python proxy.py server_port\n')
        sys.exit(2)
    
    port_num = int(sys.argv[1]) 
    
    cache_folder();    
    
    # Creating server (socket to recieve and listen)
    tcp_sock = socket(AF_INET, SOCK_STREAM)
    tcp_sock.bind(('',port_num))
    tcp_sock.listen(5)
    while 1:
        print('Request sent to serve...')
        client_sock, adr = tcp_sock.accept()
        print('Connection is received from:', adr)

        msg = receive_all(client_sock)
        msg = msg.decode()
        # print(msg)
        p = multiprocessing.Process(target=function, args=(client_sock,adr,msg))
        p.daemon = True
        p.start()




