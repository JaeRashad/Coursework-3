from tkinter import *
import csv
users = []

class View_Results(Frame):
#GUI Setup
    def __init__(self, master):
        Frame.__init__(self,master)
        self.grid()
        self.createButtons()
        self.users = []
        self.showUsers()
        self.Scroll()
        
    def showUsers(self):
        global users
        with open("users.csv") as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=",")
            for row in csv_reader:
                if row[2] == "student":
                    users.append(row[3])

    def Scroll(self):
        #scrollbar = Scrollbar()
        #scrollbar.grid(column = 1, row = 0)

        self.listbox = Listbox(self, height=3)
        for i in users:
            self.listbox.insert(END, i)
        self.listbox.grid(column = 1, row=0)

        #scrollbar.config(command=listbox.yview)

    def getUser(self):
        index = self.listbox.curselection()[0]
        studentName = str(self.listbox.get(index))
        print(studentName)

    def createButtons(self):
        nextButton = Button(self, text="select", command=self.getUser)
        nextButton.grid(column = 3,row = 1)

root = Tk()
app = View_Results(root)
root.mainloop()
