from tkinter import *

def GUI():
    class Gui(Frame):
        def __init__(self):
            #creating the window and setting its characteristics
            # Initialise the frame
            Frame.__init__(self)
            self.grid()


            self.createWidgets()

        def createWidgets(self):

            #creating a list of people who the client can connect to and letting them pick which one they want to connect to
            self.header = Label(self, bd=0, bg="white", height="1", width="37", font="Arial",text='Connect To A User:')
            self.header.grid(row=0,column=0,columnspan=5)



            self.user1=Label(self, bd=0,font="Arial",text="hey")
            self.user1.grid(row=1, column=1, sticky= W)

            userlist=['james','richard']
            userLabelList=[]
            userButtonList=[]

            for i in range(0, len(userlist),1):
                userLabelList.append(Label(self, bd=0,font="Arial",text=userlist[i]))
                userLabelList[i].grid(row=i+1,column=1, sticky= W)

                var = (Button(self, text="Connect", command=lambda: self.buttonCallBack()))
                userButtonList.append(var)
                userButtonList[i].grid(row=i+1, column=4, columnspan=1, sticky=W)

            #command=lambda:self.connect()



            self.refreshButton=Button(self, text='Refresh', command=self.refresh)
            self.refreshButton.grid(row=12, column=2, columnspan=4, sticky=W)

            # looping the window so that it will continue to stay open
            #self.text1.delete(1.0, END)

        def refresh(self):
            print('Refreshed')
            app.destroy()
            GUI()

        def buttonCallBack(self,event):
            print("hello")
            mybutton = event.widget
            text_at_row_col = mybutton["text"]

            print(text_at_row_col)

        def connect(self,user):
            """
            s.send(user.encode('utf-8'))
            connectionIP= s.recv(Buffer)
            connectionIP=connectionIP.decode('utf-8')


            z=socket.socket()
            z.connect((host,port))

            @(#$%^&%$##$%^&
            function to open the chat window
            """

            #open the chat window
            print(user)
            app.destroy()


    app=Gui()
    app.mainloop()


class Client():
    def chatWindow(self):
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

        


Client().chatWindow()