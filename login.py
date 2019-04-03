from tkinter import *
import csv
#initilize variables needed later in the application
username = str()
#read the courses the student is enrolled in
#courses = []
is_teacher = False
name = str()
loggedIn = False
class LogIn(Frame):
# GUI Setup
    def __init__ (self, master):
# Initialise Questionnaire Class
        Frame.__init__(self, master)
        self.grid()
        self.createLogin()
        #self.createButtons()
    
    def createLogin(self):
        butSubmit = Button(self, text='Log-in',font=('MS', 8,'bold'), command = self.Login)
        butSubmit.grid(row=16, column=2, columnspan=2)
        butClear = Button(self, text='Clear',font=('MS', 8,'bold'), command = self.clearResponse)
        butClear.grid(row=16, column=4, columnspan=2)
        self.entUsername = Entry(self)
        self.entUsername.grid(row=0, column=4, columnspan=2, sticky=E)
        self.entPassword = Entry(self, show='*')
        self.entPassword.grid(row=2, column=4, columnspan=2, sticky=E)
        lblCmnt = Label(self, text='User ID', font=('MS', 8,'bold'))
        lblCmnt.grid(row=0, column = 0,rowspan = 2, sticky = E)
        lblCmnt = Label(self, text='Password',font=('MS', 8,'bold'))
        lblCmnt.grid(row=2, column = 0)

    def clearResponse(self):
        self.entUsername.delete(0, END)
        self.entPassword.delete(0, END)

    def Login(self):
        failed = 1
        global username
        username = self.entUsername.get().strip()
        #user String method .upper() if usernames are stored with a capital 'C'
        #print(userID)
        password = self.entPassword.get()
        #print(len(password) * '*')
        with open('users.csv') as csvfile:
            rdr = csv.reader(csvfile)
            for row in rdr:
                #print(row[0] == username)
                #print(row)
                if row[0] == username and row[1] == password:
                    failed = 0
                    global name
                    name = row[3]
                    if row[2] == 'teacher':
                        global is_teacher
                        is_teacher = True
                    print('Welcome, {}'.format(name))
                    global loggedIn
                    loggedIn = True
                    root.destroy()
                    #return loggedIn
            if failed == 1: 
                print("LOGIN FAILED")
                self.clearResponse()
    
#Main
root = Tk()
root.title("Log In")
app = LogIn(root)
root.mainloop()
