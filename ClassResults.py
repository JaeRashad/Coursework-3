import shelve
import csv
from tkinter import *
import datetime
from dateutil import parser
from tkinter import font




class class_results(Frame):
	def __init__(self, master, students, testname):
		Frame.__init__(self, master)
		self.students = students
		self.testname = testname
		self.master.title("Class Results")
		self.grid()
		self.makeLabels()
	def makeLabels(self):

		testn = Label(self, text="Cohort results for {}".format(self.testname))
		testn.grid(row = 0, column = 0)
		StdLbl = Label(self, text="Student")
		StdLbl.grid(row = 1, column = 0, sticky = W)
		scoreLbl = Label(self, text="Score")
		scoreLbl.grid(row = 1, column = 2)
		row = 3
		for i in range(len(self.students)):
			ID = Label(self, text="{}".format(self.students[i][0]))
			ID.grid(row = row, column = 0, sticky = W)
			score = Label(self, text="{}".format(self.students[i][1]))
			score.grid(row = row, column = 2, sticky = W)
			row += 1