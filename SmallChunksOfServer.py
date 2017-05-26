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
IP = "192.168.92.203" #The Ip of the server
port = 30000 #Port the server is running on 
buffer = 1024 
applicationName = "Project Mercury" #Name of program incase GUI is added for server management


#Main server class where all functions are handled 	
class Server():

	#Init function
	def __init__(self): 
		print("Trying to Connect...")
		print("Connection has been made.")
		self.createOnlineList()
		self.waitForLogin()

	
	def createOnlineList(self):
		self.onlineList = []

	def waitForLogin(self):
		self.loginstuff = conn.recv(buffer).decode('utf-8')
		print(conn)
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
		with open("accounts.txt","r") as openfile:
			for line in openfile:
				if self.tocheck in line:
					conn.send("LoginIsGood".encode('utf-8'))
					self.onlineList.append([self.username,addr])
					for i in range(0,len(self.onlineList),1):
						self.toSend = self.onlineList[i]
						conn.send(self.toSend[1].encode('utf-8'))
					self.waitForMessages()
				else:
					conn.send("LoginIsBad".encode('utf-8'))
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
		conn.send("CreationIsGood")
		self.waitForLogin()
	
	def onlineListFunc(self):
		conn.send("Online:"+self.onlineList)


	def waitForMessages(self):
		data = None

		while True:
			self.data = conn.recv(buffer)
			# Decodes the encrypted data
			self.message = self.data.decode('utf-8')
			sendToUserIP = self.findIP(self.message)
			conn.send(sendToUserIP.encode('utf-8'))

	def findIP(self,username):
		for i in range(0, len(self.onlineList), 1):
			check = self.onlineList[i]
			usernameToCheck = check[0]
			if usernameToCheck == username:
				return check[1]


#Code that setups server and begins waiting for users to connect
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP,port))
s.listen(5)
#Server().createOnlineList()
#This code is ran whenever a new client joins the server
while True:
	conn, addr = s.accept()
	#initializses the online list where users names are stored
	
	
	#Thread that handles each client
	_start_new_thread(Server().__init__,())