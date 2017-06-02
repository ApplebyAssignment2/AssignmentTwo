"""This File is the Server file of the chat program
	It is designed to run on a server separate from the clients on its own machine
	It handles things such as:
	1. Logins and Account Creation
	2. Message handling
	3. connecting to other users
	4. Contains online user list
"""
#Import statments 
import socket #Socket is the module used for networking
from threading import _start_new_thread #threading is used to run two processes at once

#Setup variables
IP = "10.0.1.12" #The Ip of the server
port = 30000 #Port the server is running on 
buffer = 1024 
applicationName = "Project Mercury" #Name of program incase GUI is added for server management
tot_socket = 26
list_sock = []
#Main server class where all functions are handled 	
class Server():

	#Init Function
	#The contents of this function gets executed first
	def __init__(self):
		_start_new_thread(Server().__init__,())
		self.conn = conn
		self.addr = addr
		#printing the status of the connection for debugging purposeds
		print("Trying to Connect...")
		print("Connection has been made.")
		#calling the function that will create a list of users who are online at the moment
		self.createOnlineList()
		#calling the function that will wait for the client to send the login credidentials
		self.waitForLogin()

	
	def createOnlineList(self):
		#creates an empty list that we will fill in later
		self.onlineList = []

	def waitForLogin(self):
		#decoding the tuple sent by the client into a string that the program can actually interpret
		self.loginstuff = self.conn.recv(buffer).decode('utf-8')


		#if the first character in the string is a hashtag sign, then it means that the client is creating a new account
		if self.loginstuff[0] == "#":
			self.createNewLogin()
		else:
			#if they havnt sent a hashtag, the client is sending login credidentials. We call the verifyLogin() function that will
			#authenticate it
			self.verifyLogin()

	def verifyLogin(self):
		print("trying")
		#since the $ sign signifies the start of the password in the string, we will find its position with a for loop
		for i in range(0,len(self.loginstuff),1):
			if self.loginstuff[i] == "$":
				self.atpoint = i
		#the username is whateber is after the @ sign to the $ sign. Using string splices, we are storing its value in a variable
		self.username = self.loginstuff[1:self.atpoint]
		#we are doing a similar thing with the password
		self.password = self.loginstuff[self.atpoint+1:]
		#the way the user and pass are stored in our data base is conjoined together. We are gonna do the same thing with the
		#user and pass that the client has provided us with
		self.tocheck = self.username+self.password


		#opening the accountsFile to read mode
		accountsFile = open("accounts.txt","r")

		#pulling the contents of the file into a variable for futher processing
		accountsFileRead = accountsFile.readlines()
		#closing the file as we do not need it any more
		accountsFile.close()
		self.status = False
		for line in accountsFileRead:
			#checking line by line to see if the user password combo that the client sent is in the accounts file
			if self.tocheck in line:
				self.status = True
				#if it is, then the programming is adding the clients username and IP to the list of online users and then sending
				#them a list of the other users who are online
				self.onlineList.append([self.username,addr])
				self.userList = ""
				for i in range(0,len(self.onlineList),1):
					self.toSend = self.onlineList[i]
					self.userList +=self.toSend[i]+","
				self.conn.send(("Online:"+self.userList).encode('utf-8'))
				#waiting for messages from the client about future commands
				self.waitForMessages()

		#if the username and password did not match any of those in the database, then the server returns an error message
		#to the client
		if not self.status:
			self.conn.send("LoginIsBad".encode('utf-8'))
			#goes back to waiting for the login details to be sent
			self.waitForLogin()

	#function that handles the creation of new user accounts
	def createNewLogin(self):
		#goes through the string sent by server and splits into the various variables that it is meant to be and stores them
		for i in range(0,len(self.loginstuff),1):
			#this for loop sets the s
			if self.loginstuff[i] == "|":
				self.passwordpoint = i
			if self.loginstuff[i] == ">":
				self.emailpoint = i
		#creating the variables based on the start indexes determined in the for loop
		self.usernameCreate = self.loginstuff[1:self.passwordpoint]
		self.passwordCreate = self.loginstuff[self.passwordpoint+1:self.emailpoint]
		self.emailCreate = self.loginstuff[self.emailpoint+1:]

		#opening th accounts.txt file and appending the newly created user and pass to it
		with open ("accounts.txt","a") as openfile:
			openfile.write("\n"+self.usernameCreate+self.passwordCreate)
			openfile.close()

		#opening the emails.txt file and appending the email adress of the person who just registered
		with open ("emails.txt","a") as emailfile:
			emailfile.write("\n"+self.usernameCreate+self.emailCreate)
			emailfile.close()

		#sending the client a message notifying them that the account creation was successful
		self.conn.send("CreationIsGood".encode('utf-8'))
		self.waitForLogin()
	
	def onlineListFunc(self):
		self.conn.send("Online:"+self.onlineList)


	def waitForMessages(self):
		self.data = None

		while True:
			self.data = conn.recv(buffer)
			# Decodes the encrypted data
			self.message = self.data.decode('utf-8')
			#finding the users IP using the findIP() function
			sendToUserIP = self.findIP(self.message)
			#sending back the IP of the user to the client
			self.conn.send(sendToUserIP.encode('utf-8'))

	# a function that will take the name of user and return the users IP
	def findIP(self,username):
		for i in range(0, len(self.onlineList), 1):
			check = self.onlineList[i]
			usernameToCheck = check[0]
			if usernameToCheck == username:
				return check[1]


#Code that setups server and begins waiting for users to connect
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.bind((IP,port))
	s.listen(10)

#Server().createOnlineList()

#Server().createOnlineList()
#This code is ran whenever a new client joins the server
while True:

	conn, addr = s.accept()
	server  = Server().__init__()
	server.start()


	#Thread that handles each client
		