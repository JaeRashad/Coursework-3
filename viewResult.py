from tkinter import *
import csv
import shelve
import Feedback
users = []
userno = {}

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
        global userno
        with open("users.csv") as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=",")
            for row in csv_reader:
                if row[2] == "student":
                    users.append(row[3])
                    userno[row[3]] = row[0]
                    print(userno)

    def Scroll(self):
        scrollbar = Scrollbar()
        scrollbar.grid(column = 1, row = 0)

        self.listbox = Listbox(self, height=3)
        for i in users:
            self.listbox.insert(END, i)
        self.listbox.grid(column = 1, row=0)

        self.listtests = Listbox(self, height=3)
        self.listtests.grid(column = 1, row=5)
  

    def getStudentTest(self):
        global studentName
        global testType
        textbox = []
        index = self.listbox.curselection()[0]
        studentName = str(self.listbox.get(index))
        print(studentName)
        studentNo = userno[studentName]
        correctAnswers = []
        testName = []
        with open("tests_overview.csv") as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=",")
            for row in csv_reader:
                testName = row[1]
                db = shelve.open("test_results/"+testName+"_results")
                testType = row[2]
                try:
                    result = db.get(studentNo).toString()
                    db.close
                    textbox.append(testName)
                except:
                     pass
            self.listtests.delete(0, END)
            for i in textbox:
                        self.listtests.insert(END, i)

        
    def getStudentResult(self):
        index = self.listtests.curselection()[0]
        testname = str(self.listtests.get(index))
        username = userno[studentName]
        print(testname,username)
        t1 = Toplevel()
        fdbck = Feedback.Show_Results(t1, username, testname, testType, True)


        
    def createButtons(self):
        nextButton = Button(self, text="select", command=self.getStudentTest)
        nextButton.grid(column = 3,row = 1)
        resultButton = Button(self, text="select", command=self.getStudentResult)
        resultButton.grid(column = 3,row = 6)

    def turnDueDateToObject(self, testname):
    	#""" This function converts the test's duedate to a datetime.datetime object """
        print("Getting duedate and doing stuff...........")
        #> get the duedate
        duedate = [i[4] for i in test_list if i[0] == testname][0].split()
        #> split the string in to date and time
        theDate = duedate[0].split("-") #> [year, month, day]
        theTime = duedate[1].split(":") #> [hour, minute, second]
        #> create datetime object, convert values to ints as they are strings
        dueDate = datetime.datetime(int(theDate[0]), int(theDate[1]), int(theDate[2]), 
            int(theTime[0]), int(theTime[1]), int(theTime[2]))
        return dueDate


root = Tk()
app = View_Results(root)
root.mainloop()
