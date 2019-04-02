from tkinter import *
import csv
import shelve
import Feedback
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
        # get the students number to display
        global users
        global userno
        with open("users.csv") as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=",")
            for row in csv_reader:
                if row[2] == "student":
                    users.append(row[0])
                    #print(userno)

    def Scroll(self):
        # create the list boxes
        #scrollbar = Scrollbar()
        #scrollbar.grid(column = 0, row = 0, sticky=E)

        lblStudent = Label(self, text="Select a student:", font=("MS",8,"bold"))
        lblStudent.grid(row=0, column=0, columnspan=2, sticky=NW)
        self.listbox = Listbox(self, height=3)
        for i in users:
            self.listbox.insert(END, i)
        self.listbox.grid(column = 1, row=1)

        lblLists = Label(self, text="Select a test the student has taken:", font=("MS",8,"bold"))
        lblLists.grid(row=4, column=0, columnspan=2, sticky=NW)
        self.listtests = Listbox(self, height=3)
        self.listtests.grid(column = 1, row=5)
    
  

    def getStudentTest(self):
        # get the students tests they have completed
        global studentNo
        global testType
        textbox = []
        index = self.listbox.curselection()[0]
        studentNo = str(self.listbox.get(index))
        #print(studentName)
        
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
        # retrieve their results 
        index = self.listtests.curselection()[0]
        testname = str(self.listtests.get(index))
        #username = userno[studentName]
        #print(testname,username)
        #t1 = Toplevel()
        fdbck = Feedback.Show_Results(Toplevel(), studentNo, testname, testType, 0,True)


        
    def createButtons(self):
        # button creation 
        nextButton = Button(self, text="Select", command=self.getStudentTest)
        nextButton.grid(column = 3,row = 2,sticky=E)
        resultButton = Button(self, text="View Feedback", command=self.getStudentResult)
        resultButton.grid(column = 3,row = 6, sticky=E)

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

