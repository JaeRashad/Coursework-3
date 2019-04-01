import matplotlib.pyplot as plt
import numpy as np

def display_graph(attempts, students):
	testattempts = []
	studentIDs = []
	for item in attempts:
		testattempts.append(item)
	for item in students:
		studentIDs.append(item[0])
	#testattempts_class1=[35, 50, 65, 82, 90, 99]

	#timestudying= ["1638879", "1748944", "4444897", "7986755", "4757563", "5858924"]
	my_yticks = [1,2,3]
	plt.yticks(my_yticks)
	plt.scatter(studentIDs, testattempts)
	plt.title('Student Test Attempts')
	plt.ylim(0,4)
	plt.yticks(np.arange(min(testattempts), max(testattempts)+1, 1.0))
	plt.xlabel('Student Number')
	plt.ylabel('Test Attempts')
	plt.show()