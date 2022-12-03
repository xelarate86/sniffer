#!/bin/bash

#start rtl_tcp and save the PID number
/usr/local/bin/rtl_tcp &
PID=$!

#wait a few seconds to let rtl_tcp configure itself
sleep 3

#set the relative path
path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#read the info.json file for the Meter_ID
meterid=$(jq '.Meter_ID' $path/info.json)

#run rtlamr and save the output in json format
$path/rtlamr -filterid=$meterid -single=true -format='json' > reading

#run the energy_parse.py file to append the reading in a log file
python $path/energy_parse.py

#stop rtl_tcp from the PID number
kill -9 $PID

