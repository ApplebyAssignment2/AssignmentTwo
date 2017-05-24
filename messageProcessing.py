import _thread
import socket


#Setup Variables
IP = "192.168.2.76"
port = 30000
Buffer = 1024
applicationName= "Assignment 2"
connection= False
passwordVer= False
clientErrorMessage=""
global username
username= ""
global password
password= ""
sucessfulLogin= False


server='Online'
usersList=[['riaz','10.10.16.24']]


def waitForMessages(conn,addr,buffer):
    data=None

    while True:
        data = s.recv(Buffer)
        # Decodes the encrypted data
        message = data.decode('utf-8')
        sendToUserIP=findIP(message)
        conn.send(sendToUserIP.encode('utf-8'))



def findIP(username):
    for i in range(0,len(usersList),1):
        check=usersList[i]
        usernameToCheck=check[0]
        if usernameToCheck==username:
            return check[1]



while server=='Online':
    #Beginning search for clients
    print("Looking for Connections...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP,port))
    s.listen(5)
    conn, addr = s.accept()
    print(conn)
    _thread.start_new_thread(waitForMessages(conn,addr,Buffer))

