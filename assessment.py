from tkinter import *
import csv
questionlist = []


class assessment(Frame):

    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.tempno = 0
        self.master = master
        self.init_window()
        self.text()
        self.buttonPlace()

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

    def client_next(self,tempno):
        tempno += 1
        return tempno

        
    
    def client_exit(self):
        quit()

        
        '''with open("examtest.txt") as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=",")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    questionno =row[0]
                    question = row[1]
                    answer = row[2]
                    return questionno, question, answer'''
                
    def text(self):
        questionlist = self.open_file()
        tempno = 0
        text = Label(self, text="Question {}".format(questionlist[tempno][0]),font="bold")
        text.grid(row=0,column=2,pady=5)
        text2 = Label(self, text="{}".format(questionlist[tempno][1]))
        text2.grid(row=1,column=2,pady=2)

    def buttonPlace(self):
        nextButton = Button(self, text="Next", command=self.client_next)
        nextButton.grid(column = 3,row = 3,sticky=E)
        quitButton = Button(self, text="Quit", command=self.client_exit)
        quitButton.grid(column=1,row=3, sticky=E)


root = Tk()
app = assessment(root)
root.geometry("500x400")
root.mainloop()
