from tkinter import *
from tkinter import messagebox
import csv
global questionList
questionList = []
question_nr = 0
#labels = []
#time = 360000
#student = 'c1728016'

class Take_Test(Frame):
	""" 	TAKE SUMMATIVE OR FORMATIVE TEST
	"""

	def __init__(self, master, testName, timelimit, student, attempts = 0):
		Frame.__init__(self, master)
		self.testName = testName
		self.student = student
		self.timelimit = timelimit
		self.attempts = attempts
		self.get_questions()
		self.master.title(testName)
		self.initWindow()
		self.buttonPlace()
		if self.attempts == 2:
			messagebox.showwarning("Warning", "This is your final attempt!")
		global question_nr
		question_nr = 0
		global answers
		# 
		answers = [[0]*4]*len(questionList)
		#> set timelimit, number in milliseconds
		if str(self.timelimit[0]) == 'No':
			# simulates no time limit
			self.master.after(100000000000, self.timeUp)
		else:
			#> convert ['n'] in to int
			duration = int(self.timelimit[0])*60000
			print("Test Duration:",duration / 60000, "minutes")
			self.master.after(duration, self.timeUp)
	
	def timeUp(self):
		messagebox.showwarning("Time's up", "BITCH YOU RAN OUT OF TIME")
		self.submit(True)

	def initWindow(self):
		""" Initiates grid displays question 1 of the test """
		self.grid()
		global questLbl, answ1, answ2, answ3, answ4
		questLbl = Label(self, text="Question {}: {}".format(1, questionList[0][0]), font = ('Times', 14, 'bold'))
		questLbl.grid(row=0, column = 5, pady=5, columnspan = 25) # 7 kind of works
		answ1 = Label(self, text="{}".format(questionList[0][1]), font = ('MS', 10,'normal'))
		answ1.grid(row = 2, column = 6, pady = 4, columnspan = 1, sticky=W)
		answ2 = Label(self, text="{}".format(questionList[0][2]), font = ('MS', 10,'normal'))
		answ2.grid(row = 4, column = 6, pady = 4, columnspan = 1, sticky=W)
		answ3 = Label(self, text="{}".format(questionList[0][3]), font = ('MS', 10,'normal'))
		answ3.grid(row = 6, column = 6, pady = 4, columnspan = 1, sticky=W)
		answ4 = Label(self, text="{}".format(questionList[0][4]), font = ('MS', 10,'normal'))
		answ4.grid(row = 8, column = 6, pady =4 , columnspan = 1, sticky=W)
		clock = Label(self, text="You have {} minutes ".format(self.timelimit[0]), font = ('Times', 14, 'italic'))
		clock.grid(row=0, column=17, pady=5, columnspan = 8)
		self.varCB1 = IntVar()
		CB1 = Checkbutton(self, text="", variable=self.varCB1)
		CB1.grid(row=2, column=4, columnspan=1, sticky=W)
		self.varCB2 = IntVar()
		CB2 = Checkbutton(self, text="", variable=self.varCB2)
		CB2.grid(row=4, column=4, columnspan=1, sticky=W)
		self.varCB3 = IntVar()
		CB3 = Checkbutton(self, text="", variable=self.varCB3)
		CB3.grid(row=6, column=4, columnspan=1, sticky=W)
		self.varCB4 = IntVar()
		CB4 = Checkbutton(self, text="", variable=self.varCB4)
		CB4.grid(row=8, column=4, columnspan=1, sticky=W)

		#!!!!######## THIS BUTTON PLACEMENT IS AN IMPROVEMENT #########!!!!

	def buttonPlace(self): #button functionality and placement
		quitButton = Button(self, text="Quit", command=self.client_exit)
		quitButton.grid(column=0,row=11, sticky=SE, pady=2,columnspan= 1)
		submitButton = Button(self, text = "Submit Answers", command=self.submit)
		submitButton.grid(column=1, row=11, sticky=SE, pady=2, columnspan= 1) 
		nextButton = Button(self, text="\tNext", command=self.client_next)
		nextButton.grid(column = 1,row = 10,sticky=SE, columnspan= 1)
		backButton = Button(self, text="Back", command=self.client_back)
		backButton.grid(column=0,row=10, sticky=SE, columnspan= 1)
		saveButton = Button(self, text="Save Answer", command=self.on_save)
		saveButton.grid(column=3,row=10, sticky=SE, columnspan= 1)

	def actualSubmit(self):
		from Result import result 
		submission = result(self.student, answers, self.attempts)
		import shelve
		#> Test results files will be named testName_results
		db = shelve.open("test_results/"+self.testName + "_results")
		db[submission.ID] = submission
		print()
		print(submission.toString())
		#global questionList 
		#questionList = []
		print(f'Test Submitted\nUserID: {self.student}\tAttempt: {self.attempts+1} \nAnswers: {answers}')
		db.close()
		self.client_exit()

	def submit(self, isTimeUp = False):
		if isTimeUp == False:
			if messagebox.askokcancel("Submit", "Are you sure you want to submit your answers?"):
				self.actualSubmit()
		else:
			self.actualSubmit()
			
	def update(self, questionNo): 
		""" Updates labels with new question and answers"""
		global questionList
		self.varCB1.set(0)
		self.varCB2.set(0)
		self.varCB3.set(0)
		self.varCB4.set(0)
		questLbl["text"] = "Question {}: {}".format(questionNo+1, questionList[questionNo][0])
		answ1["text"] = "{}".format(questionList[questionNo][1])
		answ2["text"] = "{}".format(questionList[questionNo][2])
		answ3["text"] = "{}".format(questionList[questionNo][3])
		answ4["text"] = "{}".format(questionList[questionNo][4])
		
	def client_next(self):
		global question_nr
		
		if question_nr >= len(questionList)-1:
			messagebox.showinfo("Test","No more questions")
		else:
			question_nr += 1
			#print(question_nr+1)
			self.update(question_nr)
			
	def client_back(self):
		global question_nr

		if question_nr == 0:
			return
			#question_nr = len(questionList) - 1
			#self.update(question_nr)
		else:
			question_nr -= 1
			self.update(question_nr)
	
	
	def client_exit(self):
		#global questionList
		#questionList = []
		self.master.destroy()
	
	def on_save(self):
		global question_nr, answers
		answers[question_nr] = (self.varCB1.get(), self.varCB2.get(), self.varCB3.get(), self.varCB4.get())
		print(answers)

	def get_questions(self):
		#print("In TakeTest.py : ", self.testName)
		#print(questionList)
		print("Getting questions")
		global questionList
		questionList=[]
		with open(self.testName+".csv") as csv_file:
			csv_reader = csv.reader(csv_file,delimiter=",")
			line_count = 0
			for row in csv_reader:
				#if line_count == 0:
				#	line_count += 1
				#else:
				templist = [row[0],row[1],row[2], row[3], row[4], row[5], row[6], row[7], row[8]]
				
				#print(questionList)
				questionList.append(templist)
			
		return questionList

"""
testName = "Binary"
import shelve
#open the database
db = shelve.open("test_results/"+testName+"_results")
#check if students ID exists in database, if it returns True then do not allow student to take test if test (if test is summative)
try:
	db[student]
	messagebox.showinfo("Note", "You have already sat this test")
except KeyError:
	root = Tk()
	root.geometry("700x400")
	app = Take_Test(root, testName, 20000)
	root.mainloop()
"""





