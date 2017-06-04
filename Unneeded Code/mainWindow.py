from tkinter import *
import _thread
import time

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

                var = (Button(self, text="Connect", command=lambda row=i,: self.buttonCallBack(row)))
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

        def buttonCallBack(self,row):
            print(row)

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


GUI()
