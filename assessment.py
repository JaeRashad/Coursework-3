from tkinter import *
import csv
questionlist = []
question_nr = 0

class assessment(Frame):

    def __init__(self, master=None): #initialise variables
        Frame.__init__(self,master)
        self.tempno = 0
        self.master = master
        self.init_window()
        self.text()
        self.buttonPlace()
        self.question_nr = 0

    def init_window(self):
        self.master.title("Question")
        self.grid()
        self.entName = Entry(self)
        self.entName.grid(column=2,row=2,padx =10, pady= 10)

    def open_file(self):
        with open("examtest.txt") as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=",")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    templist = [row[0],row[1],row[2]]
                    questionlist.append(templist)
        return questionlist

    def client_next(self): #next button
        global question_nr
        print(len(questionlist))
        if question_nr >= len(questionlist)-1:
            messagebox.showinfo("test","test")
        else:
            question_nr += 1
            self.settext(question_nr,questionlist)

    def client_back(self): #back button
        global question_nr
        print(len(questionlist))
        if question_nr <= 0:
            messagebox.showinfo("test","test")
        else:
            question_nr -= 1
            self.settext(question_nr,questionlist)

        
    
    def client_exit(self): #exit button
        quit()

    def client_submit(self): #submit button
        pass

    def settext(self,question_nr,questionlist): #update question function
        text = Label(self, text="Question {}".format(questionlist[question_nr][0]),font="bold")
        text.grid(row=0,column=2,pady=5)
        text2 = Label(self, text="{}".format(questionlist[question_nr][1]))
        text2.grid(row=1,column=2,pady=2)
        
    def text(self): #sets original question
        questionlist = self.open_file()
        text = Label(self, text="Question {}".format(questionlist[0][0]),font="bold")
        text.grid(row=0,column=2,pady=5)
        text2 = Label(self, text="{}".format(questionlist[0][1]))
        text2.grid(row=1,column=2,pady=2)

    def buttonPlace(self): #button functionality and placement
        nextButton = Button(self, text="Next", command=self.client_next)
        nextButton.grid(column = 4,row = 3,sticky=E)
        quitButton = Button(self, text="Quit", command=self.client_exit)
        quitButton.grid(column=0,row=3, sticky=E)
        backButton = Button(self, text="Back", command=self.client_back)
        backButton.grid(column=3,row=3, sticky=E)
        submitButton = Button(self, text="Save Answer", command=self.client_submit)
        submitButton.grid(column=2,row=3, sticky=E)


root = Tk()
app = assessment(root)
root.geometry("500x400")
root.mainloop()
