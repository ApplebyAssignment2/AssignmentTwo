from tkinter import *


class Window():
    def GUI(self, userlist):
        print("GUI")
        self.app = Tk()
        self.__init__2(userlist)
        self.app.mainloop()

    def __init__2(self, userlist):
        # self.server.send("Hi".encode('utf-8'))
        # creating the window and setting its characteristics
        # Initialise the frame
        self.app.grid()

        self.createWidgets(userlist)

    def createWidgets(self, userlist):
        # creating a list of people who the client can connect to and letting them pick which one they want to connect to
        self.header = Label(self.app, bd=0, bg="white", height="1", width="37", font="Arial",
                            text='Connect To A User:')
        self.header.grid(row=0, column=0, columnspan=5)

        #creating a list that will hold the buttons and the labels that we create. This way, our program does not have to assign
        #names to them when we go to grid them
        userLabelList = []
        userButtonList = []

        #a for loop that goes through the amount of users there are and makes a label and button for each one of them
        for i in range(0, len(userlist), 1):
            userLabelList.append(Label(self.app, bd=0, font="Arial", text=userlist[i]))
            userLabelList[i].grid(row=i + 1, column=1, sticky=W)

            #when the button is clicked, it returns the position of the button in the list of buttons. The program uses
            #this to find out which user the "connect" button was linked to and tries to connect with them.

            var = (Button(self.app, text="Connect", command=lambda row=i:self.chatWindow()))
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

    def chatWindow(self):
        print('Chat window')
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

    def ClickAction(self):
        self.toPlace = self.EntryBox.get('1.0',END)
        # print(self.toPlace)
        self.ChatLog.config(state=NORMAL)
        self.ChatLog.insert(END,"\n"+"You: "+self.toPlace)
        self.ChatLog.config(state=DISABLED)
        self.ChatLog.yview(END)
        self.EntryBox.delete("0.0", END)

    #        self.server.send(self.EntryText.encode('utf-8'))


    def DisableEntry(self,string):
        self.EntryBox.config(state=DISABLED)


    def PressAction(self,string):
        self.EntryBox.config(state=NORMAL)
        self.ClickAction()

userlist=['riaz','Mr.Hsu','Matt']
Window().GUI(userlist)
