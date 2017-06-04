from tkinter import *


class Window():


    def chatWindow(self):
        #Creates screen
        self.Window = Tk()

        #Window Sizes
        self.Window.geometry("400x500")

        # Chat Log
        self.ChatLog = Text(self.Window, bd=0, bg="white", height="8", width="50", font="Arial", )
        self.ChatLog.insert(END, "Connecting to your partner..\n")
        self.ChatLog.config(state=DISABLED)

        # Scroll Bar
        self.scrollbar = Scrollbar(self.Window, command=self.ChatLog.yview, cursor="heart")
        self.ChatLog['yscrollcommand'] = self.scrollbar.set

        # Send button
        self.SendButton = Button(self.Window, font=30, text="Send", width="12", height=5,
                                 bd=0, bg="#FFBF00", activebackground="#FACC2E",
                                 command=self.ClickAction)

        # Entry Box where messages are typed
        self.EntryBox = Text(self.Window, bd=0, bg="white", height="8", width="50", font="Arial")

        #Allows for use of the enter button when sending messages
        self.EntryBox.bind("<Return>", self.DisableEntry)
        self.EntryBox.bind("<KeyRelease-Return>", self.PressAction)


        #Just to try something new, I fooled around with .place() and coordinates, worked pretty well in my opinion

        # Placing all of the widgets onto the screen
        self.scrollbar.place(x=376, y=6, height=386)
        self.ChatLog.place(x=6, y=6, height=386, width=370)
        self.EntryBox.place(x=128, y=401, height=90, width=265)
        self.SendButton.place(x=6, y=401, height=90)

        #Window Mainloop
        self.Window.mainloop()


    #What happens when users presses send
    def ClickAction(self):
        #Gets the message
        self.toPlace = self.EntryBox.get('1.0', END)

        #Changes log state
        self.ChatLog.config(state=NORMAL)

        #Inserts it onto the screen
        self.ChatLog.insert(END, "\n" + "You: " + self.toPlace)

        #Changes the state back to disabled
        self.ChatLog.config(state=DISABLED)

        #Scrolls down to the bottom of the screen
        self.ChatLog.yview(END)

        #Removes the text from the entry bar
        self.EntryBox.delete("0.0", END)


    def DisableEntry(self, string):
        self.EntryBox.config(state=DISABLED)


    def PressAction(self, string):
        self.EntryBox.config(state=NORMAL)
        self.ClickAction()


#Calls the functions
Window().chatWindow()