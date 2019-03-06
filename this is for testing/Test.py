#from tkinter import *
#from tkinter import messagebox
import csv

class test_file:
	""" Common base class for all test types """

	def __init__ (self, testName, module, teacherName):
		#Frame.__init__(self, master)
		open(testName+'.csv', mode='w')
		with open("tests_overview.csv", mode = 'a') as csvfile:
			csvfile.write('{},{},{}\n'.format(module, testName, teacherName))
		


