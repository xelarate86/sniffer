#!/usr/bin/python
# Script to read energy meter last reading
# 2016-04-08

import json
import time
import string
import os

#path setup
path =  os.path.dirname(os.path.realpath(__file__)) + os.path.sep	# relative directory
logfilepath  = path + 'logs' + os.path.sep				# log file directory
textfilepath = path + 'sample' + os.path.sep				# text file to read from

####### End User Variables

if not os.path.exists(logfilepath):
    os.makedirs(logfilepath)

filetimestamp = time.strftime("%Y-%m")
filename = path +  'logs/energy_' + filetimestamp + '.csv'

datafile = open(filename, "a", 1)
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

tfile = open(path+'reading')
text = tfile.read()
tfile.close()

data = json.loads(text)

kWh = float(data['Message']['Consumption']) #/ 100   #this is where you may adjust the decimal place
timestamp, _ = string.split(string.replace(data['Time'],'T',' '),'.')
stamp = str(timestamp) + ',' + str('%.2f' % kWh) + '\n'

datafile.write(stamp)
datafile.close()
