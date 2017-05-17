from tkinter import *

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