# immediate feedback for formative
import shelve
import csv
from tkinter import *
global answersInStringForm, questionList, userAnswers, correctAnswers, score

correctAnswers = []
score = 0
questionList = []
answersInStringForm = []
userAnswers = []


class Show_Results(Frame):
	""" Displays results without showing answers, for formative tests when it's not the final attempt """
	def __init__(self, master, ID, testname):
		Frame.__init__(self, master)

		self.student = ID
		self.testname = testname
		self.master.title("Results")
		
		self.get_questions()
		try:
			self.getUserAnswers()
			self.labels()
		except AttributeError:
			messagebox.showwarning("Error", "You've not taken this test.")
			self.master.destroy()
	def labels(self):

		self.grid()
		lbl1 = Label(self, text="Test: {}".format(self.testname.upper()), bg = '#55FF61',font = ('Times', 16, 'bold'))
		lbl1.grid(row=0, column = 0, sticky=W)
		lbl2 = Label(self, text="Student: {}".format(self.student.upper()), bg = '#55FF61', font = ('Times', 16, 'bold'))
		lbl2.grid(row=0, column = 1, sticky=W)
		score = self.getValues()

		lbl3 = Label(self, text="Score: {} / {} ".format(str(score), len(questionList)), font = ('Times', 16, 'italic'))
		lbl3.grid(row=0, column = 2, columnspan= 14, sticky=W)
		"""
		lbl4 = Label(self, text="Your Answer", font = ('Times', 15, 'italic'))
		lbl4.grid(row=2, column = 18)
		lbl3 = Label(self, text="Correct Answer", font = ('Times', 15, 'italic'))
		lbl3.grid(row=2, column = 9)
		q1 = Label(self, text="{}. {}.".format(1, questionList[0][0]), font = ('Times', 14, 'normal'))
		q1.grid(row=3, column=0)
		A1 = Label(text="{} /{}/{}/{}".format(questionList[0][1][0], questionList[0][1][1] if len(questionList[0][1]) >= 2 else "", 
				questionList[0][1][2] if len(questionList[0][1]) >= 3 else "", 
				questionList[0][1][3] if len(questionList[0][1]) >= 4 else ""), font = ('Times', 14,'italic'))
		A1.grid(row = 3, column = 9, sticky=W)
		"""
		row = 3
		photo1 = PhotoImage(file="good_mark.gif")	
		photo2 = PhotoImage(file="bad_mark.gif")
		for i in range(len(questionList)):
			#> this needs to be changed somehow...

			Q = Label(self, text="{}. {}-----Your Answer(s): {}\t{}\t{}\t{}".format(i+1, questionList[i][0],userAnswers[i][0], userAnswers[i][1] if len(userAnswers[i]) == 2 else "", 
				userAnswers[i][2] if len(userAnswers[i]) == 3 else "", 
				userAnswers[i][3] if len(userAnswers[i]) == 4 else ""), font = ('Times', 14, 'normal'))
			Q.grid(row=row, column = 0, sticky=NW, columnspan=15, pady = 2)
			#> Simple working answer verification for now, probably needs to be changed!!!!!
			if questionList[i][1] == userAnswers[i]:
				print(questionList[i][1],"-",userAnswers[i])
				tick = Label(self, image=photo1)
				tick.grid(row = row, column = 16)
				tick.photo = photo1	
			else:
				tick = Label(self, image = photo2)
				tick.grid(row = row, column = 16)
				tick.photo = photo2	
			row+=2
		"""
		row = 2
		for i in range(len(questionList)-1):
			Q = Label(self, text="{}. {}.    Ans: {} {} {} {}".format(i+1, questionList[i][0],questionList[i][1][0], questionList[i][1][1] if len(questionList[i][1]) == 2 else "", 
				questionList[i][1][2] if len(questionList[i][1]) == 3 else "", 
				questionList[i][1][3] if len(questionList[i][1]) == 4 else ""), font = ('Times', 14, 'italic'))
			Q.grid(row=row, column = 0, sticky=W, columnspan=10)
			row+=1
		"""
	def getUserAnswers(self):
		print("doing getUserAnswers")
		global answersInStringForm, userAnswers
		userAnswers = []
		#answersInStringForm = []
		
		data = shelve.open("test_results/" + self.testname + "_results")
		result = data.get(self.student).toString()[2]
		for i, answer in enumerate(result):
			temp = []
			for j, val in enumerate(answer):
				if val == 1:
				#print(j, val)
					temp.append(answersInStringForm[i][j])
			userAnswers.append(tuple(temp))
		data.close()
		return userAnswers
	 #> if user hasn't taken a test and tries to view the results it will return error
			#messagebox.showwarning("Error!", "You have not taken this test!")
			#print("something broke dawg")
			#self.master.destroy()

		#print(result)
		#print(type(result[0][0]))
		#print(userAnswers)

	def getValues(self):
		print("Doing getValues")
		global score, correctAnswers
		score = 0
		correctAnswers = []
		self.result = []
		self.result = shelve.open("test_results/" + self.testname + "_results").get(self.student).toString()
		#result = data.get(self.student).toString()
		with open(self.testname+".csv") as testfile:
			rdr = csv.reader(testfile)
			for row in rdr:
				correctAnswers.append((int(row[5]),int(row[6]),int(row[7]),int(row[8])))

		for i, answer in enumerate(correctAnswers):
			#print(answer)

			if self.result[2][i] == answer:
				score += 1
			print()
		#data.close()
		return score

	def get_questions(self):

		print("Getting questions")
		global questionList, answersInStringForm
		questionList=[]
		answersInStringForm = []
		with open(self.testname+".csv") as csv_file:
			csv_reader = csv.reader(csv_file,delimiter=",")
			line_count = 0
			for row in csv_reader:
				print(row)
				answersInStringForm.append((row[1], row[2], row[3], row[4]))
				tempAnsList = []
				for i in range(5,9):
					if int(row[i]) == 1:
						tempAnsList.append(row[i-4])

				questionList.append([row[0], tuple(tempAnsList)])

		#print(questionList)
		print("Asnwers in string form",answersInStringForm)
		print("questionList: ", questionList)
		return questionList	

"""
root = Tk()
a = Show_Results(root, "c1800857","Binary")
root.mainloop()
"""


