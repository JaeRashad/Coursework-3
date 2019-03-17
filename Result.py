
class result(object):
	""" This class defines a student's results for a test. It will take store student ID which will be the key, and 
	answers as one list of tuples as the value"""
	def __init__(self, ID="", answers=[], attempts=0):
		#self.count = count
		self.ID = ID
		self.answers = answers
		self.attempts = attempts

	def toString(self):
		self.attempts+=1
		return [self.ID, self.attempts, self.answers]
		