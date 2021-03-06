
#Import Statements
from tkinter import * #Tkinter for GUI
import socket #Sockets used for networking aspect of assignment
import time
from threading import _start_new_thread
import os
# Setup Variables
programName = "Project Mercury"

#Target location of connection
host = '10.0.1.12'

port = 30000
buffer = 8192
p2pPort=30001
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
        exit()
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
        exit()

    def getCreation(self):
        self.screenC.destroy()
        username = self.usernameCreationEntry.get()
        password = self.passwordCreationEntry.get()
        email = self.email.get()
        repassword = self.repasswordEntry.get()

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
        #opens a socket and connects with the said port and IP
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))



    def sendinfo(self):
        #This function takes the username and password and makes them into a form that the server can easily read and a single
        #string. It then encodes it and sends it off to the server
        self.username = "@"+self.usernameEntry.get()
        self.password = "$"+self.passwordEntry.get()
        #destroying the previous screen
        self.screenB.destroy()
        self.tosend = self.username + self.password
        print(self.tosend)
        #encoding and sending to the server
        self.server.send(self.tosend.encode('utf-8'))


    def saveInfor(self):
        # Checks if file exists
        if os.path.isfile("loginInfo.txt") == False:
            
            #Creates the window
            self.save = Tk()

            # Setup vairables
            self.save.geometry("300x300")
            self.save.title(programName)

            #Buttons and Labels   
            Label1 = Label(self.save,text = "Would you like to save your login information for later?")
            Label1.pack(side = TOP, pady = 3)
            save = Button(self.save,text = "Yes",command = self.saveToFile)
            save.pack(side = TOP,pady= 3)
            dontSave = Button(self.save,text = "No",command = self.chatWindow)
            dontSave.pack(side = TOP,pady = 3)
        else: 
            self.useLoginInfo()

        self.save.mainloop()

    def saveToFile(self):
      #Creates Login file
       saveLogin = open("loginInfo.txt","a")
       
    #Writes login data to file
       saveLogin.write(self.username + "\n" + self.password + "\n" + self.email)

    def useLoginInfo(self):
        # Not implemented as of yet.
        savedInf = open("loginInfo.txt","a")

    def TestGet(self):
        #this function interprets the data sent back by the server and call up functions accordingly
         print("Thread has started")
        #while loop
         while 1:
            print("Running")
            #stores the data that it recieves
            self.data = self.server.recv(buffer)
            #decodes it
            self.data=self.data.decode('utf-8')
            print(self.data)
            #print("Got it")
            if self.data != '':
                message=self.data
                if len(message)>5:
                    print(message[0:2])
                    #if the message it recieves says online, that means its the online list and the GUI() window needs to be
                    #refreshed or the login was sucessful
                    if message[0:2]=="On":
                        print('hi')
                        userlist=[]
                        start=0
                        #using a for loop, it processes the list which is currently in string form and it finds the different usernames and
                        #adds them to the actual userslist which is a variable in the client
                        for i in range(0,len(message),1):
                            if message[i]==':':
                                start=i

                            if message[i]==',':
                                start+=1
                                userlist.append(message[start:i])
                                start=i

                        #tries to destory the GUI screen incase it was already there(this happens during a refresh). If it cant because
                        #the GUI screen doesnt exist, then it just keeps going instead of crashing
                        try:
                            self.screenA.destroy()
                            self.GUI.destroy()
                        except:
                            print('no window')

                        #starts a thread that will constantly be looking for people to connect
                        self.GUI(userlist)
                        _start_new_thread(self.waitForP2P())

                #deals with the other possible comands that could be sent from the server and calls up functions accordingly
                if self.data == "LoginIsBad":
                    self.loginScreen()
                    self.screenB.destroy()
                if self.data == "CreationIsGood":
                    self.login()
            
            else:
                #if there is a command that this function did not understand gets sent, it prints it out for debugging purposes
                print(self.data.decode('utf-8'))


    def chatWindow(self,conn,IP,user):

        self.Window = Tk()

        self.Window.geometry("400x500")

        #Chat Log
        self.ChatLog = Text(self.Window, bd=0, bg="white", height="8", width="50", font="Arial",)
        self.ChatLog.insert(END, "Connecting to your partner..\n")
        self.ChatLog.config(state=DISABLED)

        #Scroll Bar
        self.scrollbar = Scrollbar(self.Window, command=self.ChatLog.yview, cursor="heart")
        self.ChatLog['yscrollcommand'] = self.scrollbar.set

        #Send
        self.SendButton = Button(self.Window, font=30, text="Send", width="12", height=5,
                    bd=0, bg="#FFBF00", activebackground="#FACC2E",
                    command=self.ClickAction)

        #Entry Box where messages are typed
        self.EntryBox = Text(self.Window, bd=0, bg="white",height="8", width="50", font="Arial")
        self.EntryBox.bind("<Return>",self.DisableEntry)
        self.EntryBox.bind("<KeyRelease-Return>",self.PressAction)

        #Placing on screen
        self.scrollbar.place(x=376,y=6, height=386)
        self.ChatLog.place(x=6,y=6, height=386, width=370)
        self.EntryBox.place(x=128, y=401, height=90, width=265)
        self.SendButton.place(x=6, y=401, height=90)

        self.Window.mainloop()

        _start_new_thread(self.insertRecievedMessages, (buffer, user))

    def p2pConnect(self,IP,p2pPort):
        self.p2p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p2p.connect((IP, p2pPort))

    def insertRecievedMessages(self,buffer,user):
        self.data=self.p2p.recv(buffer)
        self.message = self.data.decode('utf-8')
        self.ChatLog.config(state=NORMAL)
        self.ChatLog.insert(END,"\n"+user+": "+self.message)
        self.ChatLog.config(state=DISABLED)
        self.ChatLog.yview(END)


    def ClickAction(self):
        self.toPlace = self.EntryBox.get('1.0',END)
        # print(self.toPlace)
        self.ChatLog.config(state=NORMAL)
        self.ChatLog.insert(END,"\n"+"You: "+self.toPlace)
        self.ChatLog.config(state=DISABLED)
        self.ChatLog.yview(END)
        self.EntryBox.delete("0.0", END)
        self.p2p.send(self.EntryBox.encode('utf-8'))
    

    def DisableEntry(self,string):
        self.EntryBox.config(state=DISABLED)
    

    def PressAction(self,string):
        self.EntryBox.config(state=NORMAL)
        self.ClickAction()

    def GUI(self,userlist):
        print("GUI")
        self.app = Tk()
        self.screenB.destroy()
        self.__init__2(userlist)
        self.app.mainloop()
        
            
    def __init__2(self,userlist):
        #self.server.send("Hi".encode('utf-8'))
        # creating the window and setting its characteristics
        # Initialise the frame
        self.app.grid()

        self.createWidgets(userlist)

    def createWidgets(self,userlist):
        # creating a list of people who the client can connect to and letting them pick which one they want to connect to
        self.header = Label(self.app, bd=0, bg="white", height="1", width="37", font="Arial",
                                text='Connect To A User:')
        self.header.grid(row=0, column=0, columnspan=5)

        self.user1 = Label(self.app, bd=0, font="Arial", text="hey")
        self.user1.grid(row=1, column=1, sticky=W)


        #creating a list that will hold the buttons and the labels that we create. This way, our program does not have to assign
        #names to them when we go to grid them

        userLabelList = []
        userButtonList = []

        # a for loop that goes through the amount of users there are and makes a label and button for each one of them
        for i in range(0, len(userlist), 1):
            userLabelList.append(Label(self.app, bd=0, font="Arial", text=userlist[i]))
            userLabelList[i].grid(row=i + 1, column=1, sticky=W)

            #when the button is clicked, it returns the position of the button in the list of buttons. The program uses
            #this to find out which user the "connect" button was linked to and tries to connect with them.

            var = (Button(self.app, text="Connect", command=lambda row=i: self.p2pconnect(i)))
            userButtonList.append(var)
            userButtonList[i].grid(row=i + 1, column=4, columnspan=1, sticky=W)

        # a refresh button that when called, closes the window and opens it again with a refreshed list of users

        self.refreshButton = Button(self.app, text='Refresh', command=self.refresh)
        self.refreshButton.grid(row=12, column=2, columnspan=4, sticky=W)

            # looping the window so that it will continue to stay open
            # self.text1.delete(1.0, END)

    def refresh(self):
        print('Refreshed')
        self.app.destroy()
        self.GUI()

    def p2pconnect(self, user):
        self.server.send(user)
        connectionIP=self.recv(buffer)
        connectionIP=connectionIP.decode('utf-8')
        self.chatWindow(connectionIP,user)


    def waitForP2P(self):
        loop=True
        while loop:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((socket.gethostname(), p2pPort))
            s.listen(5)
            conn,addr=s.accept()
            user='Unknown'
            self.chatWindow(conn,addr,user)

#initializing the chat client
Client().__init__()


