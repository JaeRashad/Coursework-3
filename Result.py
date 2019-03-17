
class result(object):
	""" This class defines a student's results for a test. It will take store student ID which will be the key, and 
	answers as one list of tuples as the value"""
	def __init__(self, ID="", answers=[]):
		#self.count = count
		self.ID = ID
		self.answers = answers
	
	def toString(self):
		return f'{self.ID}\n{self.answers}'