import matplotlib.pyplot as plt

testscores_class1=[35, 50, 65, 82, 90, 99]

timestudying= ["1638879", "1748944", "4444897", "7986755", "4757563", "5858924"]

plt.scatter(timestudying, testscores_class1)

plt.title('Student Test Grades')
plt.xlabel('Student Number')
plt.ylabel('Test Scores')
plt.show()