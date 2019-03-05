from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import csv
import login
import os
#import CreateTest
#Note for later self: check if a test name with the same name exists when creating a test. Maybe also add a timer so it gets deleted automatically

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
            self.listProg.selection_set(END)

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
        test_list = []
        with open('tests_overview.csv') as csvfile:
            rdr = csv.reader(csvfile)
            for row in rdr:
                if row[0] == module:#Might need to add in the fact that a test gets taken
                    test_list.append(row[1])
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
                    self.listTest.insert(END, test)
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
            CreateTest.Create_Test(t1, testfile+'.csv')
        else:
            messagebox.showwarning("ERROR", "Please a pick an existing test to edit.")
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
            # if testName isn't None or "" AND the file doesn't already exist 
            if testName and os.path.isfile('.\\{}.csv'.format(testName)) == False: 
                import Test
                #t1 = Toplevel()
                #t1.title("Test")
                Test.test_file(testName, strModule, name)
                print('Test Created\nTest Name: {0:20}Teacher: {1:20}\n'.format(testName, name))
            elif testName:
                messagebox.showwarning("ERROR", "Test with that name already exists!")
            else:
                messagebox.showwarning("ERROR", "You must provide a test name")
        else:
            messagebox.showwarning("ERROR", "Please select a module!")

    def takeTest(self):
        pass
#mainloop
if login.username != "":
    root = Tk()
    root.title("HOME "+ str(login.username))
    app = Welcome(root)
    root.mainloop()
    
