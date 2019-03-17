from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

import csv
import login
import os
#import CreateTest
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
        scroll.grid(row=3, column=7, sticky=W)
        modules_list = self.retrieveModules()
        for module in modules_list:
            self.listProg.insert(END, module)
            #self.listProg.selection_set(END)

        self.listTest = Listbox(self, height= 3)
        scroll = Scrollbar(self, command= self.listTest.yview)
        self.listTest.configure(yscrollcommand=scroll.set)
        self.listTest.grid(row=7, column=0, columnspan=2, sticky=NE)
        scroll.grid(row=7, column=7, sticky=W)
        
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
                #print(row[0])
                if row[0] == module:#Might need to add in the fact that a test gets taken
                    #> row[4] is test duration, adding it to test_list mean the duration vars are more accessible 
                    test_list.append((row[1], row[4])) 
        if len(test_list) == 0:
            # rather than return empty list, return -1
            return -1
        else:
            return test_list

    def createButtons(self):
        butCheck = Button(self, text='Check for Tests',font=('MS', 8,'bold'), command=self.checkTest)
        butCheck.grid(row=4, column=0, columnspan=2)
        if login.is_teacher:
            butCreate = Button(self, text='Create TEST!',font=('MS', 8,'bold'), command=self.createTest)
            butCreate.grid(row=8, column=0, columnspan=2)
            butEdit = Button(self, text='Edit Test', font=('MS', 8,'bold'), command=self.editTest)
            butEdit.grid(row = 8, column = 3, columnspan=2)
        else:
            butTake = Button(self, text='Take TEST!',font=('MS', 8,'bold'), command = self.takeTest)#rename me to thing depending on whether or not you are a teacher
            butTake.grid(row=8, column=0, columnspan=2)

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
            import CreateTest
            index = self.listTest.curselection()[0]
            testfile = str(self.listTest.get(index))
            # Try - Except can be used if neccessary
            #try:
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
            import CreateTest
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
                return
            testType = simpledialog.askstring("Input", "Formative Test: F, Summative Test: S")
            if testType and testType.upper() == 'S':
                testDuration = simpledialog.askinteger("Input", "Enter the test duration time in minutes.\n (Min: 15, Max: 120)")
                if testDuration < 15:
                    #> change testDuration to 15 
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
                import Test
                #t1 = Toplevel()
                #t1.title("Test")
                Test.test_file(testName, testType.upper(), strModule, name, testDuration)
                print('...Test Created...\n'+120*'-'+'\nTest Name: {0:30}Type: {1:10}Teacher: {2:25}Duration: {3:9}\n'.format(testName, 'Formative' if testType.upper() == 'F' else 'Summative', 
                    name, 'No time limit' if testType.upper() == 'F' else str(testDuration) + ' minutes'))
                self.checkTest()
                self.editTestFast(testName)
                #print(test_list)
            elif testName:
                messagebox.showwarning("ERROR", "Test with that name already exists!")
                return
            else:
                messagebox.showwarning("ERROR", "Something went wrong?!")
                return
        else:
            messagebox.showwarning("ERROR", "Please select a module!")
            return

    def takeTest(self):
        index = self.listTest.curselection()[0]
        testName= str(self.listTest.get(index))
        print("Taking Test:", testName)
        import shelve
        #> open the database situated in the test_results folder.
        #> 
        #> Retrieve test duration
        timeLimit = [i[1] for i in test_list if i[0] == testName]
        #print(timeLimit)
        db = shelve.open("test_results/"+testName+"_results")
        #check if students ID exists in database, if it returns True then do not allow student to take test if test (if test is summative)
        try:
            db[login.username]
            messagebox.showinfo("Note", "You have already sat this test")
            db.close()
        except KeyError:
            db.close()
            import TakeTest
            t1 = Toplevel()
            t1.geometry("600x500")
            app = TakeTest.Take_Test(t1, testName, timeLimit, login.username)
            



#mainloop
if login.username != "":
    root = Tk()
    root.title("HOME "+ str(login.username))
    app = Welcome(root)
    root.mainloop()
    
