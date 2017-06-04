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
buffer = 8192
applicationName = "Project Mercury" #Name of program incase GUI is added for server management
tot_socket = 26
list_sock = []

#Main server class where all functions are handled 	
class Server():

	#Init function
	def __init__2(self): 
		print("Connection has been made.")
		self.createOnlineList()
		self.waitForLogin()

	
	def createOnlineList(self):
		self.onlineList = []

	def waitForLogin(self):
		print("here 4")
		self.loginstuff = self.conn.recv(buffer).decode('utf-8')
		print(self.loginstuff)
		if self.loginstuff[0] == "#":
			self.createNewLogin()
		else:
			self.verifyLogin()

	def verifyLogin(self):
		print("trying")
		for i in range(0,len(self.loginstuff),1):
			if self.loginstuff[i] == "$":
				self.atpoint = i
		self.username = self.loginstuff[1:self.atpoint]
		self.password = self.loginstuff[self.atpoint+1:]
		self.tocheck = self.username+self.password
		
		accountsFile = open("accounts.txt","r")
		accountsFileRead = accountsFile.readlines()
		accountsFile.close()
		self.status = False
		for line in accountsFileRead:
			if self.tocheck in line:
				self.status = True	
				self.onlineList.append([self.username,self.addr])
				self.userList = ""
				for i in range(0,len(self.onlineList),1):
					self.toSend = self.onlineList[i]
					self.userList +=self.toSend[i]+","
				
				self.conn.send(("Online:"+self.userList).encode('utf-8'))
				print("sent")
				self.waitForMessages()
		if not self.status:
			self.conn.send("LoginIsBad".encode('utf-8'))
			self.waitForLogin()


	def createNewLogin(self):
		for i in range(0,len(self.loginstuff),1):
			if self.loginstuff[i] == "|":
				self.passwordpoint = i
			if self.loginstuff[i] == ">":
				self.emailpoint = i
		self.usernameCreate = self.loginstuff[1:self.passwordpoint]
		self.passwordCreate = self.loginstuff[self.passwordpoint+1:self.emailpoint]
		self.emailCreate = self.loginstuff[self.emailpoint+1:]
		with open ("accounts.txt","a") as openfile:
			openfile.write("\n"+self.usernameCreate+self.passwordCreate)
			openfile.close()		
		with open ("emails.txt","a") as emailfile:
			emailfile.write("\n"+self.usernameCreate+self.emailCreate)
			emailfile.close()
		self.conn.send("CreationIsGood".encode('utf-8'))
		self.waitForLogin()
	
	def onlineListFunc(self):
		self.conn.send("Online:"+self.onlineList)


	def waitForMessages(self):


			self.data = self.conn.recv(buffer)
			#Decodes the encrypted data
			self.message = self.data.decode('utf-8')
			sendToUserIP = self.findIP(self.message)
			self.conn.send(sendToUserIP.encode('utf-8'))
			print()

	def findIP(self,username):
		for i in range(0, len(self.onlineList), 1):
			check = self.onlineList[i]
			usernameToCheck = check[0]
			if usernameToCheck == username:
				return check[1]

	def __init__(self):
	#Code that setups server and begins waiting for users to connect
		print("Started")
		self.list_sock = []
		
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.bind((IP,port))
		s.listen(10)
		print("Here 1")
		self.list_sock.append(s)
			#print("Trying to Connect...")
			#Server().createOnlineList()

			#Server().createOnlineList()
			#This code is ran whenever a new client joins the server
		while True:
			for i in range(len(self.list_sock)):
				print(self.list_sock)
				print("Here 3")
				self.conn, self.addr = self.list_sock[i].accept()
				print ('Connected with')
		#initializses the online list where users names are stored
	
	
		#Thread that handles each client
				_start_new_thread(self.__init__2,())
		#s.close()
		
Server().__init__()