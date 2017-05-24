#Import statements
import socket
import _thread
import datetime

#configuring time settings
now = datetime.datetime.now()

#opening the accounts file so that it can be read
accountsFile=open('accounts.txt','r')
logFile=open('connectionLogs.txt','w')

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



def waitForClient():
    #Beginning search for clients
    print("Looking for Connections...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP,port))
    s.listen(5)
    conn, addr = s.accept()

    logFile.write("["+now.strftime("%Y-%m-%d %H:%M")+"] Connection from",addr)
    #making a new thread so that the program can keep searching for new connections
    #_thread.start_new_thread(passwordVerification(),args=(conn,addr))

    passwordVerification(conn,addr)

#this function will authenticate the username and password of the user
def passwordVerification(conn,addr):

    #waiting for the password to be sent
    while True:
        # waiting for the client to send the username and password
        jumble = conn.recv(Buffer)

        
        #seperating the variable sent by the client into a username and a password variable
        
        jumble=str(jumble)
        print(jumble)
        newJumble=jumble[2:len(jumble)]
        
        for i in range(0,len(newJumble),1):
            #the $ sign means that it is the password. Therefore whatever is before it is the username
            if newJumble[i]=='$':
                username=newJumble[0:i]
                password=newJumble[i:len(newJumble)-1]

               
        print (username)
        print (password)
        #finding the special username and password signs and using them to 

        #checking if the string sent by the client starts with '@'. The client attaches an '@' sign to all usernames and
        #password
        if username[0]!="@":
            clientErrorMessage=="notExpectedUsername"

            #sending an error message to the client letting them know why they have been denied access to the chat systems
            conn.send(clientErrorMessage.encode('utf-8'))
            pass

        #checking if a password has been sent by seeing if it has the '@' sign
        if password[0]!='$':
            clientErrorMessage == "notExpectedPassword"

            # sending an error message to the client letting them know why they have been denied access to the chat systems
            conn.send(clientErrorMessage.encode('utf-8'))
            pass

        if username[0]=='@' and password[0]== '$':
            # if both a username and a password has been sent to the server than it will continue with the verification process
            #this will break out of the while loop
            # this is for debugging purposes

            print("The user who is trying to connect:", username)
            print("The password they have entered:", password)

            break





    #we will now call up our username and password dictionairy to verify the users credidentials

    #first, we are checking if the username that the client entered is even in our database
    #reading the file and making its contents into a variable so that we can proccess it

    accountsContent = accountsFile.read()
    accountsUsername=None
    realPassword=""

    for i in range(0, len(accountsContent), 1):
        if accountsContent[i] == '@':
            start = i
            print('start', start)
        elif accountsContent[i] == '$':
            end = i
            print('end', end)
            accountsUsername = accountsContent[start:end]

            print(accountsUsername)

            if accountsUsername == username:
                for i in range(end, len(accountsContent), 1):
                    if accountsContent[i] == '@':
                        realPassword = accountsContent[end:(i - 1)]
                        print(realPassword)
                        break

    print('username:', username)
    print('password entered:', password)
    print('actual pass', realPassword)

    if accountsUsername!=None:


        #if the password is correct, then a message is said to the client and the user is allowed to start sending messages
        if password==realPassword:
            sucessfulLogin=True
            clientSuccessMessage=('passwordVerSucessful')
            conn.send(clientSuccessMessage.encode('utf-8'))

            #calling the main menu function
            Messages(Buffer,conn,addr)


        #if the password is incorrect, then the login process starts again
        else:
            clientErrorMessage == "notCorrectPassword"

            # sending an error message to the client letting them know why they have been denied access to the chat systems
            conn.send(clientErrorMessage.encode('utf-8'))

            passwordVerification(conn,addr)

    #if the username isnt even in the directory, then the server lets the client know
    else:
        clientErrorMessage == "notExpectedUsername"

        # sending an error message to the client letting them know why they have been denied access to the chat systems
        conn.send(clientErrorMessage.encode('utf-8'))

        #restarting the password verification function so that the user will be allowed to re-enter their credidentials
        passwordVerification()


#this function triggers the main menu where the user will be allowed to do a variety of actions
def main():
    None


#Function for receiving messages from client
def Messages(Buffer,conn,addr):
    #Prints the connecting address, of the client
    print("Connection Address: ",addr)
    while True:
        data = conn.recv(Buffer)
        #Decodes the encrypted data
        message = data.decode('utf-8')
        #If client types "quit" the server shuts down
        if message == "Quit":
            conn.close()
            raise SystemExit
        else:
            print("Data:", message)

        data = input(">>>")
        conn.send(data.encode('utf-8'))

#Introduction to threading, still learning about this
#_thread.start_new_thread(waitForClient())

#Runs the program
waitForClient()


"""

	def verifyLogin(self):
		for i in range(0,len(self.loginstuff),1):
			if self.loginstuff[i] == "$":
				self.atpoint = i
		self.username = self.loginstuff[1:self.atpoint]
		self.password = self.loginstuff[self.atpoint+1:]
		self.tocheck = self.username+self.password
		with open("accounts.txt","r") as openfile:
			for line in openfile:
				if self.tocheck in line:
					self.conn.send("Good Login".encode('utf-8'))


	def createNewLogin(self):
		for i in range(0,len(self.loginstuff),1):
			if self.loginstuff[i] == "|":
				self.passwordpoint = i
			if self.loginstuff[i] == ">":
				self.emailpoint = i
		self.usernameCreate = self.loginstuff[1:self.passwordpoint]
		self.passwordCreate = self.loginstuff[self.passwordpoint+1:self.emailpoint]
		self.emailCreate = self.loginstuff[self.emailpoint+1:]
		print(self.usernameCreate,self.passwordCreate,self.emailCreate)

"""

