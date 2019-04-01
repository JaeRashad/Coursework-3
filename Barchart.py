#Data for Bar chart
#student: C1845458  correct: 9  incorrect: 1
#student: c4854215  correct: 6  incorrect: 4
#student: c1485745  correct: 2  incorrect: 8
#student: c1247856  correct: 9  incorrect: 1
#student: c4121655  correct: 4  incorrect: 6
#student: c1535856  correct: 7  incorrect: 3


import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#student = {'Name': ,
 #          'id': ,
  #         'Grades':
   #     }
   
data1 = {'Student': ['c1858485', 'c1264854', 'c1877512', 'c1765482'],
         'Grades%' : [68,71,24,96]
    }   

df1 = DataFrame(data1, columns = ['Student', 'Grades%'])
df1 = df1[['Student', 'Grades%']].groupby('Student').sum()

root= tk.Tk()


figure1 = plt.Figure(figsize=(6,5), dpi=100)
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, root)
bar1.get_tk_widget().pack(side = tk.LEFT, fill=tk.BOTH)
df1.plot(kind='bar', legend=True, ax=ax1)
ax1.set_title('Student grades Percentages')



root.mainloop()
