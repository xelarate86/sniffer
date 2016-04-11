import matplotlib
matplotlib.use('Agg') #required for saving the figure through an SSH connection

import matplotlib.pyplot as plt
import csv
from datetime import datetime
import time
import os

# find the relative dir and set the file path
path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep 
filetimestamp = time.strftime("%Y-%m")
filename = path +  'logs/energy_' + filetimestamp + '.csv'

# initiate the x and y arrays
x = []
y = []

# open and reat the .csv file by appending the data
with open(filename,'rb') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(datetime.strptime(str(row[0]), '%Y-%m-%d %H:%M:%S'))
        y.append(float(row[1]))

# create the figure
fig, ax = plt.subplots()
ax.plot(x, y)
fig.autofmt_xdate()

plt.xlabel('Time')
plt.ylabel('kWh')
plt.title('EECE 7364 - Mobile and Wireless Systems\nSmart Meter Readings')
ax.get_yaxis().get_major_formatter().set_useOffset(False)
plt.savefig(path + 'meter_readings.png')
