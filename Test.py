#from tkinter import *
#from tkinter import messagebox
import csv

class test_file:
	""" Common base class for all test types """

	def __init__ (self, testName, testType, module, teacherName, timeLimit):
		#Frame.__init__(self, master)
		open(testName+'.csv', mode='w')
		if testType == 'F':
			self.attemptsAllowed = 3
		else:
			self.attemptsAllowed = 1
		with open("tests_overview.csv", mode = 'a') as csvfile:
			csvfile.write('{},{},{},{},{},{}\n'.format(module, testName, testType, teacherName, timeLimit, self.attemptsAllowed))
		


