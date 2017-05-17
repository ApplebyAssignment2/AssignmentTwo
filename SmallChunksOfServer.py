import socket
from threading import _start_new_thread
IP = "10.10.19.21"
port = 30000
buffer = 1024
applicationName = "Project Mercury"
	
class Server():
	def __init__(self): 
		print("Trying to Connect...")
		print("Connection has been made.")
		self.waitForLogin()



	def waitForLogin(self):
		self.loginstuff = conn.recv(buffer).decode('utf-8')
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

				else:
					conn.send("LoginIsBad".encode('utf-8'))
					self.waitForLogin


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
		with open ("accounts.txt","a") as openfile:
			openfile.write("\n"+self.usernameCreate+self.passwordCreate)
			openfile.close()
		with open ("emails.txt","a") as emailfile:
			emailfile.write("\n"+self.usernameCreate+self.emailCreate)
			emailfile.close()
	def messageHandling(self):
		print()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP,port))
s.listen(5)

while 1:
	conn, addr = s.accept()
	_start_new_thread(Server().__init__,())