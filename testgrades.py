import matplotlib.pyplot as plt
import numpy as np

def display_graph(attempts, students):
	testattempts = attempts
	studentIDs = students
	"""
	for item in attempts:
		testattempts.append(item)
	for item in students:
		studentIDs.append(item[0])"""
	#testattempts_class1=[35, 50, 65, 82, 90, 99]

	#timestudying= ["1638879", "1748944", "4444897", "7986755", "4757563", "5858924"]


	plt.scatter(studentIDs, testattempts)
	plt.title('Percentage of time question answered correctly')
	#plt.ylim(-5,105)
	plt.yticks(np.arange(min(testattempts), 105, 10.0))
	plt.xticks(np.arange(min(studentIDs), max(studentIDs)+1, 1.0))
	plt.xlabel('Question Number')
	plt.ylabel('Percentage of Students')
	plt.show()
