from tkinter import * #Tkinter for GUI
import socket #Sockets used for networking aspect of assignment
import time
import base64
from threading import _start_new_thread
import os
# Setup Variables
programName = "Project Mercury"

#Target location of connection
host = '10.0.1.12'

port = 30000
buffer = 8192
p2pPort=30001
user="Zayd"
#The main Client class
class Client(Frame):
    #Init function, ran on start up
    def __init__(self,):
        try:
            #Attempts to connect to server and opens login window

            self.connect()
            _start_new_thread(self.TestGet, ())
            self.loginScreen()
            print('Waiting for server...')
            #Error window if cannot connect to server
            
        except ConnectionRefusedError:

            #Creates error window
            self.error = Tk()

            #Error window setups
            self.error.geometry("300x100")
            self.error.title(programName)

            #Error label
            self.errorMessage = Label(self.error,text = "Could not connect to server\n Please try again later.",font = ('Helvetica', 14))
            self.errorMessage.pack()

            #Error window loop
            self.error.mainloop()
            exit()
        #Login screen that first asks user if they are new or returning
    def loginScreen(self):
        if os.path.isfile("loginInfo.txt") == False:

            #Creates window
            self.screenA = Tk()
            
            #Setup variables
            self.screenA.geometry("250x200")
            self.screenA.title(programName)

            #Label
            self.account = Label(self.screenA,text = "Do you have an account already?")
            self.account.pack(side = TOP)


            #Yes and No buttons
            self.loginOption = Button(self.screenA,text = "Yes", command = self.loginDe)
            self.loginOption.pack(side = BOTTOM, pady = 3)

            self.newOption = Button(self.screenA,text = "No",command = self.newAccount)
            self.newOption.pack(side = BOTTOM, pady = 3)

            #Window loop
            self.screenA.mainloop()
            exit()
            #self.screenA.destroy()
        else:
            self.useLoginInfo()

    def loginDe(self):
        self.screenA.destroy()
        self.login()

    def login(self):

        #Creates the login screen for usernames and password input
        self.screenB = Tk()
        

        #Usual setup variables
        self.screenB.geometry("250x200")
        self.screenB.title(programName)

        #Intro Label
        self.credentials = Label(self.screenB,text = "Enter your username and password")
        self.credentials.pack(side = TOP,pady = 10)

        #Username Information
        self.usernameLabel = Label(self.screenB,text = "Username:")
        self.usernameLabel.pack(side = TOP, pady= 3)
        self.usernameEntry = Entry(self.screenB)
        self.usernameEntry.pack(side = TOP, pady = 3)

        # Password Information
        self.passwordLabel = Label(self.screenB,text = "Password:")
        self.passwordLabel.pack(side = TOP, pady= 3,)
        self.passwordEntry = Entry(self.screenB,show = '*')
        self.passwordEntry.pack(side = TOP, pady = 3)

        # Login Button
        self.loginButton = Button(self.screenB,text = "Login",command = self.sendinfo)
        self.loginButton.pack(side = TOP,pady = 3)

        #Window loop
        self.screenB.mainloop()
        

    def newAccount(self):
        #Creates the window
        self.screenC = Tk()
        self.screenA.destroy()

        #Screen settings
        self.screenC.geometry("300x400")
        self.screenC.title(programName)

        #Top Label
        self.creationLabel = Label(self.screenC,text = "Complete the fields below to create an account")
        self.creationLabel.pack(side = TOP,pady = 5)

        #Username Creation
        self.usernameCreation = Label(self.screenC,text = "Enter your username:")
        self.usernameCreation.pack(side = TOP,pady = 5)

        self.usernameCreationEntry = Entry(self.screenC)
        self.usernameCreationEntry.pack(side = TOP, pady = 3)

        # Email Creation
        self.email = Label(self.screenC,text = "Enter your email: ")
        self.email.pack(side = TOP, pady = 3)

        self.email = Entry(self.screenC)
        self.email.pack(side = TOP,pady = 3)


        # Password Creation
        self.passwordCreation = Label(self.screenC,text = "Enter your password: ")
        self.passwordCreation.pack(side = TOP, pady = 3)

        self.passwordCreationEntry = Entry(self.screenC)
        self.passwordCreationEntry.pack(side = TOP,pady = 3)

        #Re-enter password
        self.repassword = Label(self.screenC, text = "Re-enter your password: ")
        self.repassword.pack(side = TOP,pady = 3)

        self.repasswordEntry = Entry(self.screenC)
        self.repasswordEntry.pack(side = TOP, pady = 3)

        # Create Button
        signup = Button(self.screenC,text = "Create",command = self.getCreation)
        signup.pack(side = TOP,pady = 3)

        #Window Loop
        self.screenC.mainloop()
      

    def getCreation(self):

        username = self.usernameCreationEntry.get()
        password = self.passwordCreationEntry.get()
        email = self.email.get()
        repassword = self.repasswordEntry.get()
        self.screenC.destroy()
        # If re-entering the password does not match the the original password
        if password != repassword:
            #Creates error window
            self.passwordMatch = Tk()
            #Setup variables
            self.passwordMatch.geometry("300x200")
            self.passwordMatch.title(programName)

            # Error label
            self.match = Label(self.passwordMatch,text = "Passwords do not match")
            self.match.pack(side = TOP)

            #Window loop
            self.passwordMatch.mainloop()
            time.sleep(2)

        # Checks if any of the fields have been left blank
        if username == "" or password == "" or email == "":

            # Creates error window
            self.usernameMatch = Tk()

            # Setup variables
            self.usernameMatch.geometry("300x200")
            self.usernameMatch.title(programName)

            # Error label
            self.match = Label(self.usernameMatch, text="One of the fields has been left empty")
            self.match.pack(side=TOP)

            # Window loop
            self.usernameMatch.mainloop()

        #Prepares to send the information to the server, where it will go through a checking process

        self.finalUsername = '#'+username
        self.finalPassword = '|'+password
        self.finalEmail = ">"+email
        self.finalCreation = self.finalUsername + self.finalPassword + self.finalEmail

        self.server.send(self.finalCreation.encode('utf-8'))
        



    #Function the begins connection with the server

    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    def sendinfo(self):
        
        self.username = "@"+self.usernameEntry.get()
        self.password = "$"+self.passwordEntry.get()
        self.screenB.destroy()
        self.tosend = self.username + self.password
        print(self.tosend)
        self.server.send(self.tosend.encode('utf-8'))
        time.sleep(10)
    def TestGet(self):
             print("Thread has started")
             while 1:
                #Gets data from the server
                self.data = self.server.recv(buffer)
                self.data=self.data.decode('utf-8')

                #Makes sure there is something  in the data
                if self.data != '':
                    message=self.data

                    #Process to detect the online users
                    if len(message)>5:
                        if message[0:2]=="On":

                            userlist=[]
                            start=0

                           #Splits online users from what was sent from the server and adds it to a list
                            for i in range(0,len(message),1):
                                if message[i]==':':
                                    start=i

                                if message[i]==',':
                                    start+=1
                                    userlist.append(message[start:i])
                                    start=i

                            #Calls the Online List GUI
                            self.GUI(userlist)
                            try:
                                self.screenA.destroy()
                            except:
                                print('no window')

                    #If server tells client that login did not work
                    if self.data == "LoginIsBad":

                        #Brings user back to login screen
                        self.loginScreen()
                        self.screenB.destroy()
                    #If user account creation was good, brings them to login screen
                    if self.data == "CreationIsGood":
                        self.login()


    #Outlines of the online list GUI
    def GUI(self, userlist):

        #Creates window
        self.app = Tk()
        #Calls this fucntion the create rest of window
        self.__init__2(userlist)

        #Mainloop
        self.app.mainloop()


    def __init__2(self, userlist):

        # creating the window and setting its characteristics
        # Initialise the frame

        self.app.grid()
        self.app.title(programName)
        #Calls createWidgets to add the online users to the screen
        self.createWidgets(userlist)


    def createWidgets(self, userlist):
        # creating a list of people who the client can connect to and letting them pick which one they want to connect to

        #Headers
        self.header = Label(self.app, bd=0, bg="white", height="1", width="37", font="Arial",
                            text='Connect To A User:')
        self.header.grid(row=0, column=0, columnspan=5)

        self.user1 = Label(self.app, bd=0, font="Arial", text="hey")
        self.user1.grid(row=1, column=1, sticky=W)


        #Empty List
        userLabelList = []
        userButtonList = []


        #Goes through the user list and depending on the amount of users creates the amount of rows required to store them
        #all on one screen
        for i in range(0, len(userlist), 1):
            userLabelList.append(Label(self.app, bd=0, font="Arial", text=userlist[i]))
            userLabelList[i].grid(row=i + 1, column=1, sticky=W)

            #For the example, connect button is broken
            var = (Button(self.app, text="Connect", command=lambda row=i: self.p2pconnect(i)))
            userButtonList.append(var)
            userButtonList[i].grid(row=i + 1, column=4, columnspan=1, sticky=W)

        self.refreshButton = Button(self.app, text='Refresh', command=self.refresh)
        self.refreshButton.grid(row=12, column=2, columnspan=4, sticky=W)



    #Refresh function that is supposed to get the list from the server to update online list, not working in example
    def refresh(self):
        print('Refreshed')
        self.app.destroy()
        self.GUI()
Client().__init__()