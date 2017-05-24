#Import statements
import socket
# Setup Variables
Message = ''
#IP & Port the client is connecting to
IP = '192.168.2.76'
Port = 30000
Buffer = 1024

#Makes the connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP,Port))

#Allows user to send unlimited messages to the server
while Message != '':
    Message = input("enter text: ")
    s.send(Message.encode('utf-8'))
    data=s.recv()
    message = data.decode('utf-8')
    print(message)

