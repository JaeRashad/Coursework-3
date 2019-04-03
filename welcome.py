from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from dateutil import parser
import datetime
import TakeTest, Feedback, CreateTest, login, Test
import csv
import os
import shelve
#Note for later self: check if a test name with the same name exists when creating a test. Maybe also add a timer so it gets deleted automatically
test_list = []


class Welcome(Frame):
# GUI Setup
    def __init__ (self, master):
# Initialise Questionnaire Class
        Frame.__init__(self, master)
        self.grid()
        self.overView()
        self.createButtons()
    def overView(self):
        lblQuestion = Label(self, text = 'WELCOME '+login.name, font=('MS', 8,'bold'))
        lblQuestion.grid(row=0, column= 4, rowspan=2)
        # Create widgets to select a module from a list
        string = ""
        if login.is_teacher:
            string = "Modules you can create an assesment in"
        else:
            string = "Modules you may have assesments in"
        lblModules = Label(self, text=string, font=('MS', 8,'bold'))
        lblModules.grid(row=2, column=0, columnspan=2, sticky=NE)  
        self.listProg = Listbox(self, height= 3)
        scroll = Scrollbar(self, command= self.listProg.yview)
        self.listProg.configure(yscrollcommand=scroll.set)
        self.listProg.grid(row=3, column=0, columnspan=2, sticky=NE)
        scroll.grid(row=3, column=4, sticky=W)
        modules_list = self.retrieveModules()
        for module in modules_list:
            self.listProg.insert(END, module)
            #self.listProg.selection_set(END)

        self.listTest = Listbox(self, height= 3)
        scroll = Scrollbar(self, command= self.listTest.yview)
        self.listTest.configure(yscrollcommand=scroll.set)
        self.listTest.grid(row=7, column=0, columnspan=2, sticky=NE)
        scroll.grid(row=7, column=4, sticky=W)
        
    def retrieveModules(self):
        modules_list = []
        with open('user_modules.csv') as csvfile:
            rdr = csv.reader(csvfile)
            for row in rdr:
                #print(row)
                #print("Does {} == {}".format(row[0], login.username))
                if row[0] == login.username:
                    for i in range(1,len(row)):
                        if row[i]!= "":
                            modules_list.append(row[i])
        return modules_list
    def retrieveTests(self, module):
        global test_list # setting it to be global so i can access it within Create_Test
        test_list = []
        with open('tests_overview.csv') as csvfile:
            rdr = csv.reader(csvfile)
            for row in rdr:
                if row[0] == module:#Might need to add in the fact that a test gets taken
                    
                        #> row[4] is TEST DURATION, adding it to test_list mean the duration vars are more accessible
                        #> row[5] is ATTEMPTS  allowed - 1 for summative, 3 for formative
                        #> row[2] is TEST TYPE
                        #print("row 6:", row[6])
                        #print("row 6 type", type(row[6]))
                    print(row)
                    if row[2] == "F":
                        test_list.append((row[1], row[4], row[5], row[2]))
                    else:
                    	#> STORE THE DUEDATE AT INDEX 4 OF THE TUPLE
                        test_list.append((row[1], row[4], row[5], row[2], row[6]))
                    #else:
                    #    print("row 6:", row[6])
                    #    test_list.append((row[1], row[4], row[5], row[2], row[6]))
        if len(test_list) == 0:
            # rather than return empty list, return -1
            return -1
        else:
            return test_list
    def getIndividualResults(self):
        import viewResult

        viewResult.View_Results(Toplevel())

    def createButtons(self):
        butCheck = Button(self, text='Check for Tests',font=('MS', 8,'bold'), command=self.checkTest)
        butCheck.grid(row=4, column=0, columnspan=2)
        if login.is_teacher:
            butCreate = Button(self, text='Create TEST!',font=('MS', 8,'bold'), command=self.createTest)
            butCreate.grid(row=8, column=0, columnspan=2)
            butEdit = Button(self, text='Edit Test', font=('MS', 8,'bold'), command=self.editTest)
            butEdit.grid(row = 8, column = 3, columnspan=2)
            butView = Button(self, text='View Class results', font=('MS', 8,'bold'), command=self.viewClassResults)
            butView.grid(row = 8, column = 6, columnspan=2)
            butIndv = Button(self, text='View Individual Results', font=('MS', 8,'bold'), command=self.getIndividualResults)
            butIndv.grid(row = 8, column = 9, columnspan=2)

        else:
            butTake = Button(self, text='Take TEST!',font=('MS', 8,'bold'), command = self.takeTest)#rename me to thing depending on whether or not you are a teacher
            butTake.grid(row=8, column=0, columnspan=2)
            butResult = Button(self, text='View Result',font=('MS', 8,'bold'), command = self.getResult)
            butResult.grid(row=8, column=3, columnspan=2)

    def viewClassResults(self):
        if self.listTest.curselection() != ():
            index = self.listTest.curselection()[0]
            testname = str(self.listTest.get(index))
            db = shelve.open("test_results/"+testname+"_results")
            students = []
            attempts = []
            all_students = [[]]
            position = 0
            total = 0
            for item in db:
                students.append(item)
            for i in range(len(students)):
                results = db.get(students[i]).toString()[2]
                #attempts.append(db.get(students[i]).toString()[1])
                score = 0
                correctAnswers = []
                result = db.get(students[i]).toString()
                #> Get the answers to the questions and store in var correctAnswers
                with open(testname+".csv") as testfile:
                        rdr = csv.reader(testfile)
                        for row in rdr:
                                correctAnswers.append((int(row[5]),int(row[6]),int(row[7]),int(row[8])))
                #> iterate through the answers and enumerate them,
                for b, answer in enumerate(correctAnswers):
                    if result[2][b] == answer:
                        score += 1
                        all_students[position].append(1)
                    else:
                        all_students[position].append(0)
                all_students.append([])
                position += 1
                students[i] = (students[i], score)
            question_x = [0]*(len(all_students[0]))
            all_students.pop(len(all_students)-1)
            try:
                for i in range(len(all_students[0])):
                    for student in all_students:
                        question_x[i] += student[i]

                question_list = []
                for i in range(len(question_x)):

                    question_x[i] = round(question_x[i]/len(all_students)*100, 1)
                    question_list.append(i+1)
                print(all_students)
                print(question_x)
                
                import testgrades
                import ClassResults
                classResult = ClassResults.class_results(Tk(), students, testname)
                testgrades.display_graph(question_x, question_list)
            except IndexError:
                messagebox.showwarning("Note", "No students have taken this test yet!")


        
        
    def checkTest(self):
        """ This function appends the tests available for a give 
                module to the Listbox listTest
        """
        
        if self.listProg.curselection() != ():#Check if the user has selected something
            index = self.listProg.curselection()[0]
            strModule = str(self.listProg.get(index))
            #retrieve tests for that module
            test_list = self.retrieveTests(strModule)
            # i.e. if retrieveTests doesn't return -1
            if test_list != -1:
                self.listTest.delete(0,END)
                for test in test_list:
                    self.listTest.insert(END, test[0])
                    self.listTest.selection_set(END)
            else:
                #clear list box and show message
                self.listTest.delete(0,END)
                messagebox.showwarning("Note!","There are no tests for that module. ")
        else:
            messagebox.showwarning("ERROR","Please select a module!")

    def editTest(self):
        if self.listTest.curselection() != ():
            t1 = Toplevel()
            t1.title("Test")

            index = self.listTest.curselection()[0]
            testfile = str(self.listTest.get(index))
            # Try - Except can be used if neccessary
            #try:
            CreateTest.create_file = 1
            CreateTest.Create_Test(t1, testfile+'.csv')
            #except FileNotFoundError:
            #    messagebox.showwarning("ERROR", "Test only exists in tests_overview.csv")
            #    t1.destroy()
        else:
            messagebox.showwarning("ERROR", "Please a pick an existing test to edit.")
    def editTestFast(self, testfile):
        if self.listTest.curselection() != ():
            t1 = Toplevel()
            t1.title("Test")
            
            CreateTest.Create_Test(t1, testfile+'.csv')
    def createTest(self):
        """ This method creates an empty test csv file with a filename specified by the user in a 
            dialog box that appears. It then appends the test's metadata (teacher, testname, module) 
            to the tests_overview.csv file """
        
        if self.listProg.curselection() != ():
            index = self.listProg.curselection()[0]
            strModule = str(self.listProg.get(index))
            #print(strModule)
            name = login.name
            testName = simpledialog.askstring("Input", "Enter test name")
            #if testname == None or contains forbidden characters 
            if not testName or len([i for i in testName if i in ['/', '\\', '?', '%', '*', ':', '|', '"', '<', '>', '.']]) != 0:
                messagebox.showinfo("Error", "You didn't enter a name or you \nused a forbidden character!")
                
            testType = simpledialog.askstring("Input", "Formative Test: F, Summative Test: S")
            duedate = False
            if testType and testType.upper() == 'S':

                invalid_input=True
                while(invalid_input==True):
                    dueDate = simpledialog.askstring("Input", "Please enter the date the assesment is due in a following format 'Aug 28 1999 12:00AM'")
                    try:
                        duedate = parser.parse(dueDate)
                        now = datetime.datetime.now()
                        print((now-duedate).total_seconds())
                        if (now-duedate).total_seconds() > 0:
                            messagebox.showwarning("ERROR", "Please enter a date that's in the future")
                        else:
                            invalid_input=False
                    except:
                        messagebox.showwarning("ERROR", "Enter the due date in a valid format")

                
                testDuration = simpledialog.askinteger("Input", "Enter the test duration time in minutes.\n (Min: 15, Max: 120)")
                if testDuration < 15:
                    #> change testDuration to 15 
                    #testDuration = 15
                    pass 
                elif testDuration > 120:
                    testDuration = 120
            elif testType and testType.upper() == 'F':
                #> Formative tests don't need time limits so setting testDuration 
                #> to be several years is a solution for now
                testDuration = 'No' # in milliseconds
            else:
                messagebox.showwarning("ERROR", "Enter F or S!")
                return



            
            # check if the file already exists in the folder or if testName for the selected module is already in tests_overview
            if os.path.isfile('.\\{}.csv'.format(testName)) == False and testName not in test_list:
                
                
                if duedate == False:
                    Test.test_file(testName, testType.upper(), strModule, name, testDuration)
                else:
                    Test.test_file(testName, testType.upper(), strModule, name, testDuration, duedate)
                print('...Test Created...\n'+120*'-'+'\nTest Name: {0:30}|Type: {1:10}|Teacher: {2:25}|Duration: {3:9}\n'.format(testName, 'Formative' if testType.upper() == 'F' else 'Summative', 
                    name, 'No time limit' if testType.upper() == 'F' else str(testDuration) + ' minutes' + str(duedate)))
                self.checkTest()
                self.editTestFast(testName)
                #print(test_list)
            elif testName:
                messagebox.showwarning("ERROR", "Test with that name already exists!")
                
            else:
                messagebox.showwarning("ERROR", "Something went wrong?!")
                
        else:
            messagebox.showwarning("ERROR", "Please select a module!")
            

    def takeTest(self):
        if self.listTest.curselection() != ():
            index = self.listTest.curselection()[0]
            testName= str(self.listTest.get(index))
            print("Taking Test:", testName)
            
            #> open the database situated in the test_results folder.
            #> 
            #> Retrieve test duration
            timeLimit = [i[1] for i in test_list if i[0] == testName]
            attemptsAllowed = [i[2] for i in test_list if i[0] == testName]
            testType = [i[3] for i in test_list if i[0] == testName]
            testType = str(testType[0]) #> convert it to a string
            print("attemptsAllowed =",attemptsAllowed[0])
            print("testType =",testType)
            db = shelve.open("test_results/"+testName+"_results")
            #check if students ID exists in database, if it returns True then do not allow student to take test if test (if test is summative)
            try:
                if testType == 'S':
                    """WE only have test name to work on :( so i have to check all of the test_overview file for the datetime
                    
                    #> Duedate is saved in test_list as the 4th index so don't need this 
                    with open('tests_overview.csv') as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        for row in csv_reader:
                            if row[1] == testName:
                                dueDate = row[6]
                    """
                    #duedate = parser.parse(dueDate)
                    duedate = self.turnDueDateToObject(testName) #> Dis be quicker! 
                    now = datetime.datetime.now()
                    if now>duedate:#current due date has passed :( therefore don't allow student to take test
                        messagebox.showinfo("TOO LATE!!!","Sorry, the due date for this assesment has passed already")
                    else:
                        db[login.username]
                        messagebox.showinfo("Can't take summative test!", "You have already sat this test")
                    db.close()

                elif testType == 'F':
                    db[login.username]
                    attempts = db.get(str(login.username)).toString()[1]
                    print("You have made {} attempts so far".format(attempts))
                    if attempts == 3:
                        messagebox.showinfo("Can't take formative test!", "You have already used your final attempt")
                        db.close()
                    else:
                        db.close()
                        t1 = Toplevel()
                        t1.geometry("700x300")
                        app = TakeTest.Take_Test(t1, testName, timeLimit, login.username, testType, attempts)  
                        
            except KeyError: # if database for test doesn't contain student's userID, it will return KeyError
                db.close()
                t1 = Toplevel()
                t1.geometry("700x300")
                app = TakeTest.Take_Test(t1, testName, timeLimit, login.username, testType)
        else:
            messagebox.showwarning("ERROR", "Please select a test to take!")

    def getResult(self):
        if self.listTest.curselection() != ():
            index = self.listTest.curselection()[0]
            testname = str(self.listTest.get(index))
            testType = [i[3] for i in test_list if i[0] == testname]
            testType = str(testType[0])
            t1 = Toplevel()
            if testType == 'S':
                #> this is horrible...
                duedate = self.turnDueDateToObject(testname)
                print(duedate)
                fdbck = Feedback.Show_Results(t1, login.username, testname, testType, duedate)
            elif testType == 'F':
                fdbck = Feedback.Show_Results(t1, login.username, testname, testType)
            else:
                messagebox.showwarning("Error", "Is your testtype a string other than 'F' or 'S'?")
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
#mainloop
#if login.username != "":
if login.loggedIn != False:
    root = Tk()
    root.title("HOME "+ str(login.username))
    app = Welcome(root)
    root.mainloop()
    
