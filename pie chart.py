from tkinter import *
import tkinter  as tk
import matplotlib.pyplot as plt

labels = 'Correct', 'Incorrect'
sizes = [71, 29]
colors = ['green', 'red']
explode= (0.1, 0)
answer_cor = [6]
answer_inc = [4]

plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct= '%1.1f%%', shadow = True)

plt.axis('equal')
plt.show()