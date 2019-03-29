from tkinter import *
from tkinter import messagebox
import csv
questionNumber = 1
create_file = 0
saved_questions=[]

#filename=str()
#def createTest():

class Create_Test(Frame):
# GUI Setup
    def __init__ (self, master, filename):
# Initialise Questionnaire Class
        self.filename = filename
        self.load_saved_questions()
        Frame.__init__(self, master)
        self.grid()
        self.createTest()
        self.createButtons()
    def createTest(self):
        global questionNumber
        global saved_questions
        lblQuestion = Label(self, text = 'Question ' + str(questionNumber), font=('MS', 8,'bold'))
        lblQuestion.grid(row=3, column= 4, rowspan=2)
        self.Question = Text(self, height=3,width=40)
        scroll = Scrollbar(self, command=self.Question.yview)
        self.Question.configure(yscrollcommand=scroll.set)
        self.Question.grid(row=12, column=2,columnspan=5, sticky=E)
        scroll.grid(row=12, column=7, sticky=W)
        lblAnswer = Label(self, text = 'Choice 1', font=('MS', 8,'bold'))
        lblAnswer.grid(row=13, column= 4, rowspan=2)
        #rename this
        self.Answer1 = Text(self, height=1,width=40)
        self.Answer1.grid(row=16, column=2,columnspan=5, sticky=E)
        lblAnswer = Label(self, text = 'Choice 2', font=('MS', 8,'bold'))
        lblAnswer.grid(row=17, column= 4, rowspan=2)
        self.Answer2 = Text(self, height=1,width=40)
        self.Answer2.grid(row=20, column=2,columnspan=5, sticky=E)
        lblAnswer = Label(self, text = 'Choice 3', font=('MS', 8,'bold'))
        lblAnswer.grid(row=21, column= 4, rowspan=2)
        self.Answer3 = Text(self, height=1,width=40)
        self.Answer3.grid(row=24, column=2,columnspan=5, sticky=E)
        lblAnswer = Label(self, text = 'Choice 4', font=('MS', 8,'bold'))
        lblAnswer.grid(row=25, column= 4, rowspan=2)
        self.Answer4 = Text(self, height=1,width=40)
        self.Answer4.grid(row=28, column=2,columnspan=5, sticky=E)
        
        self.isQuestionSaved()
        
        #self.varCB1 = IntVar()
        CB1 = Checkbutton(self, text="Correct Question", variable=self.varCB1)
        CB1.grid(row=13, column=5, columnspan=1, sticky=W)
        
        #rename this
        #self.varCB2 = IntVar()
        CB2 = Checkbutton(self, text="Correct Question", variable=self.varCB2)
        CB2.grid(row=17, column=5, columnspan=1, sticky=W)
        
        #rename this
        #self.varCB3 = IntVar()
        CB3 = Checkbutton(self, text="Correct Question", variable=self.varCB3)
        CB3.grid(row=21, column=5, columnspan=1, sticky=W)
        
        #rename this
        #self.varCB4 = IntVar()
        CB4 = Checkbutton(self, text="Correct Question", variable=self.varCB4)
        CB4.grid(row=25, column=5, columnspan=1, sticky=W)
        
        #print(counter)
        #print(questionNumber)

    def load_saved_questions(self):
        r = csv.reader(open(self.filename, 'a+')) 
        #> Changed write mode from r to a+ because it was giving an 
        #> error when clicking Edit Test for tests that exist in tests_overview.csv 
        #> but don't actually have an existing file yet. 
        old = list(r)
        temp_questionNum = 0
        try:
            for line in old:
                temp_questionNum += 1
                saved_questions.appned(temp_questionNum)
        except:
            return

    def isQuestionSaved(self):
        tests_list = self.retrieveTests()
        for number in saved_questions:
            if questionNumber == number:
                self.printTextBox(True)
                return
        for test in tests_list:
            if test == self.filename[:-4]:
                self.printTextBox(True)
                return
        self.printTextBox(False)
    
    def printTextBox(self, saved):
        if saved == True:
            with open(self.filename) as test:
                r = csv.reader(test)
                if questionNumber != 1:
                    for i in range(questionNumber - 1):
                        try:
                            next(r)
                        except:
                            self.printTextBox(False)
                            return
                try:
                    data = next(r)
                except:
                        self.printTextBox(False)
                        return
                self.Question.insert(END, data[0])
                self.Answer1.insert(END, data[1])
                self.Answer2.insert(END, data[2])
                self.Answer3.insert(END, data[3])
                self.Answer4.insert(END, data[4])
                self.varCB1 = IntVar(value=int(data[5]))
                self.varCB2 = IntVar(value=int(data[6]))
                self.varCB3 = IntVar(value=int(data[7]))
                self.varCB4 = IntVar(value=int(data[8]))
        else:
            self.Question.insert(END, "INPUT QUESTION HERE")
            self.Answer1.insert(END, "INPUT FIRST CHOICE HERE")
            self.Answer2.insert(END, "INPUT SECOND CHOICE HERE")
            self.Answer3.insert(END, "INPUT THIRD CHOICE HERE")
            self.Answer4.insert(END, "INPUT FOURTH CHOICE HERE")
            self.varCB1 = IntVar()
            self.varCB2 = IntVar()
            self.varCB3 = IntVar()
            self.varCB4 = IntVar()

    def retrieveTests(self):
        tests_list = []
        counter = 0
        with open('tests_overview.csv') as csvfile:
            rdr = csv.reader(csvfile)
            for row in rdr:
                if counter == 0:
                    counter = 1
                else:
                    tests_list.append(row[1])
                    
        return tests_list
        

    def createButtons(self):
        butNextQuestion = Button(self, text='Next Question',font=('MS', 8,'bold'))
        butNextQuestion['command']=self.nextQuestion
        butNextQuestion.grid(row=30, column=4, columnspan=1)

        butPreviousQuestion = Button(self, text='Previous Question',font=('MS', 8,'bold'))
        butPreviousQuestion['command']=self.previousQuestion
        butPreviousQuestion.grid(row=30, column=2, columnspan=2)

        butSave = Button(self, text='Save',font=('MS', 8,'bold'))
        butSave['command']=self.saveQuestion
        butSave.grid(row=30, column=5, columnspan=2)

        butClear = Button(self, text='Clear',font=('MS', 8,'bold'))
        butClear['command']=self.clearResponse
        butClear.grid(row=30, column=7, columnspan=2)

        """butNextQuestion = Button(self, text='Next Question',font=('MS', 8,'bold'))
        butSave['command']=self.saveTest
        butSave.grid(row=30, column=6, columnspan=2)"""
        
    def nextQuestion(self):
        global questionNumber
        r = csv.reader(open(self.filename, 'r'))
        old = list(r)
        if self.Question.get("1.0", "end-1c").replace(",","").replace("\n"," ") == "INPUT QUESTION HERE" or self.Question.get("1.0", "end-1c").replace(",","").replace("\n"," ") == "":
            messagebox.showwarning("Note!", "Please fill out the question before proceeding!")
            return
        try:
            if old[questionNumber-1][0] != self.Question.get("1.0", "end-1c").replace(",","").replace("\n"," "):
                messagebox.showwarning("Note!", "You have made a change to question number: " + str(questionNumber) + "\n Please save your changes before you continue")
                return
            if old[questionNumber-1][1] != self.Answer1.get("1.0", "end-1c").replace(",","").replace("\n"," "):
                messagebox.showwarning("Note!", "You have made a change to question number: " + str(questionNumber) + "\n Please save your changes before you continue")
                return
            if old[questionNumber-1][2] != self.Answer2.get("1.0", "end-1c").replace(",","").replace("\n"," "):
                messagebox.showwarning("Note!", "You have made a change to question number: " + str(questionNumber) + "\n Please save your changes before you continue")
                return
            if old[questionNumber-1][3] != self.Answer3.get("1.0", "end-1c").replace(",","").replace("\n"," "):
                messagebox.showwarning("Note!", "You have made a change to question number: " + str(questionNumber) + "\n Please save your changes before you continue")
                return
            if old[questionNumber-1][4] != self.Answer4.get("1.0", "end-1c").replace(",","").replace("\n"," "):
                messagebox.showwarning("Note!", "You have made a change to question number: " + str(questionNumber) + "\n Please save your changes before you continue")
                return

        except:
            messagebox.showwarning("Note!", "Please save the question before proceeding!")
            return

        if self.Answer1.get("1.0", "end-1c").replace(",","").replace("\n"," ") == "INPUT FIRST CHOICE HERE" or self.Answer1.get("1.0", "end-1c").replace(",","").replace("\n"," ") == "":
            messagebox.showwarning("Note!", "Please fill out the answers before proceeding!")
            return
        if self.Answer2.get("1.0", "end-1c").replace(",","").replace("\n"," ") == "INPUT FIRST CHOICE HERE" or self.Answer2.get("1.0", "end-1c").replace(",","").replace("\n"," ") == "":
            messagebox.showwarning("Note!", "Please fill out the answers before proceeding!")
            return
        if self.Answer3.get("1.0", "end-1c").replace(",","").replace("\n"," ") == "INPUT FIRST CHOICE HERE" or self.Answer3.get("1.0", "end-1c").replace(",","").replace("\n"," ") == "":
            messagebox.showwarning("Note!", "Please fill out the answers before proceeding!")
            return
        if self.Answer4.get("1.0", "end-1c").replace(",","").replace("\n"," ") == "INPUT FIRST CHOICE HERE" or self.Answer4.get("1.0", "end-1c").replace(",","").replace("\n"," ") == "":
            messagebox.showwarning("Note!", "Please fill out the answers before proceeding!")
            return
        if self.varCB1.get() == 0 and self.varCB2.get() == 0 and self.varCB3.get() == 0 and self.varCB4.get() == 0:
            messagebox.showwarning("Note!", "Please select the correct answer and SAVE before proceeding!")
            return
        questionNumber += 1
        self.createTest()

    def previousQuestion(self):
        global questionNumber
        if questionNumber == 1:
            return
        questionNumber -= 1
        self.createTest()

    def saveQuestion(self):
        global questionNumber
        global create_file
        global saved_questions
        if create_file != 0:
            r = csv.reader(open(self.filename, 'r'))
            old = list(r)
            if questionNumber > len(old):
                with open(self.filename, mode='a') as csv_file:
                    csv_file.write(self.Question.get("1.0", "end-1c").replace(",","").replace("\n"," ")+",")
                    csv_file.write(self.Answer1.get("1.0","end-1c").replace(",","").replace("\n"," ")+",")
                    csv_file.write(self.Answer2.get("1.0","end-1c").replace(",","").replace("\n"," ")+",")
                    csv_file.write(self.Answer3.get("1.0","end-1c").replace(",","").replace("\n"," ")+",")
                    csv_file.write(self.Answer4.get("1.0","end-1c").replace(",","").replace("\n"," ")+",")
                    csv_file.write(str(self.varCB1.get())+",")
                    csv_file.write(str(self.varCB2.get())+",")
                    csv_file.write(str(self.varCB3.get())+",")
                    csv_file.write(str(self.varCB4.get())+"\n")
                saved_questions.append(questionNumber)
            else:
                old[questionNumber-1][0] = (self.Question.get("1.0", "end-1c").replace(",","").replace("\n"," "))
                old[questionNumber-1][1] = (self.Answer1.get("1.0", "end-1c").replace(",","").replace("\n"," "))
                old[questionNumber-1][2] = (self.Answer2.get("1.0", "end-1c").replace(",","").replace("\n"," "))
                old[questionNumber-1][3] = (self.Answer3.get("1.0", "end-1c").replace(",","").replace("\n"," "))
                old[questionNumber-1][4] = (self.Answer4.get("1.0", "end-1c").replace(",","").replace("\n"," "))
                old[questionNumber-1][5] = (str(self.varCB1.get()))
                old[questionNumber-1][6] = (str(self.varCB2.get()))
                old[questionNumber-1][7] = (str(self.varCB3.get()))
                old[questionNumber-1][8] = (str(self.varCB4.get()))
                with open(self.filename, 'w') as writer:
                    for i in old:
                        length = 1
                        for x in i:
                            if length < len(i):
                                writer.write(x + ",")
                                length += 1
                            else:
                                writer.write(x)
                        writer.write("\n")
        else:
            with open(self.filename, mode='a') as csv_file:
                csv_file.write(self.Question.get("1.0", "end-1c").replace(",","").replace("\n"," ")+",")
                csv_file.write(self.Answer1.get("1.0","end-1c").replace(",","").replace("\n"," ")+",")
                csv_file.write(self.Answer2.get("1.0","end-1c").replace(",","").replace("\n"," ")+",")
                csv_file.write(self.Answer3.get("1.0","end-1c").replace(",","").replace("\n"," ")+",")
                csv_file.write(self.Answer4.get("1.0","end-1c").replace(",","").replace("\n"," ")+",")
                csv_file.write(str(self.varCB1.get())+",")
                csv_file.write(str(self.varCB2.get())+",")
                csv_file.write(str(self.varCB3.get())+",")
                csv_file.write(str(self.varCB4.get())+"\n")
            saved_questions.append(questionNumber)
            create_file += 1

    def clearResponse(self):
       self.Question.delete("1.0", END)
       self.Answer1.delete("1.0", END)
       self.Answer2.delete("1.0", END)
       self.Answer3.delete("1.0", END)
       self.Answer4.delete("1.0", END)



#Main
"""
This isn't need as we can use Toplevel 
root = Tk()
root.title("Create Test")
app = Create_Test(root)
root.mainloop()
"""
