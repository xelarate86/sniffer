# EECE 7364 - SDR Examples with the Raspberry Pi
Tyler Fenton is Master of Science Candidate at [Northeastern University](http://www.northeastern.edu/) in the [College of Electrical and Computer Engineering](http://www.ece.neu.edu/). This material was produced by Tyler for [Professor Chowdhury's](http://krc.coe.neu.edu/) Mobile and Wireless Networks course (EECE 7364, Spring 2016).

### Introduction
This guide takes you through the steps needed to set up a Linux computer with a USB SDR module, and gives several examples of the software possibilities. These steps should work for most distributions of Linux, and many of the various options for USB SDR modules. However, the specific setup used in this guide is as follows:
* [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) ($35)
* [Micro SD Card (8 GB or more](http://www.amazon.com/SanDisk-microSDHC-Standard-Packaging-SDSQUNC-032G-GN6MA/dp/B010Q57T02/ref=sr_1_2?ie=UTF8&qid=1459631933&sr=8-2&keywords=micro+sd+32) ($10)
* [Raspbian Jessie (Release Date 2016-03-18)](https://www.raspberrypi.org/downloads/raspbian/) ($0)
* [NooElec NESDR Nano 2](http://www.amazon.com/NooElec-NESDR-Nano-RTL2832U-Compatible/dp/B018PUYPCA/ref=sr_1_6?ie=UTF8&qid=1459631753&sr=8-6&keywords=nooelec) ($20)

## Raspberry Pi
The first step is getting the Raspberry Pi up and running with a network connection, which is out of the scope of this tutorial. There are tutorials and guides on installing Raspbian to the SD card and booting the OS available online. You may use a keyboard and monitor with the Pi, or configure ssh access to log in remotely. Some useful links are: 
* [raspberrypi.org - Installing OS Images](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
* [circuitbasics.com - How to Setup a Raspberry Pi Without a Monitor or Keyboard](http://www.circuitbasics.com/raspberry-pi-basics-setup-without-monitor-keyboard-headless-mode/)

#### Getting Started
This tutorial operates from the command line. Be sure to open a terminal to execute all the following commands. It also assumes you are running everything from a default Raspbian (Rasberry Pi Debian) Linux image, and that your home directory is ```/home/pi```. Everything should work on a similar Linux distribution, but you will need to change the relative paths to fit your environment. 
   
Make sure you expand the Filesystem to allow full use of the SD Card.
```
sudo raspi-config
```
Follow the prompts to select the first option. 
```
Expand Filesystem
```
Select ```<Finish>``` and ```<Yes>``` to reboot the system.

#### Dependencies
Once you have followed these steps and have internet access from your Raspberry Pi, you should ensure your OS is up-to-date.
```
sudo apt-get update
sudo apt-get upgrade
```
Now is a good time to install all the required dependencies for the tutorial.
```
sudo apt-get install cmake libusb-1.0-0-dev golang jq python-matplotlib
```
You may also want to set the system time to the local time zone:
```
sudo dpkg-reconfigure tzdata
```

If you are able to run the above successfully, you are now ready to begin the SDR portion.

## SDR - Software Defined Radio
There are many applications for a SDR (software defined radio), with hardware options ranging form entry to professional levels. This guide uses a DVB-T (Digital Video Broadcasting — Terrestrial) USB tuner. Originally these pieces of hardware were designed to receive OTA (over the air) television broadcasts for viewing on your computer. However, due to their extremely low cost and versatile hardware, they gained popularity in the open-source community. This tutorial will cover one of the many examples available online. The projects we will focus on are **[RTL-SDR](http://sdr.osmocom.org/trac/wiki/rtl-sdr)** and **[RTLAMR](https://github.com/bemasher/rtlamr)**. **RTL-SDR** is the software that interfaces with the SDR hardware. In our example it creates an open TCP connection with ```rtl_tcp``` and transfers the raw I/Q samples to the localhost. **RTLAMR** receives the samples over this connection and completes the signal processing on the [ERT protocol](https://en.wikipedia.org/wiki/Encoder_receiver_transmitter). This allows us to capture the meter values from all smart readers in the area. A quick block diagram from **RTLARM** is given below, with further explanation available on [bemasher's github site](http://bemasher.github.io/rtlamr/signal.html).
![signal flow](http://bemasher.github.io/rtlamr/assets/signal_flow.png)

### RTL-SDR

At this point the USB dongle should be plugged into your Raspberry Pi.  
  
Download the ```RTL-SDR``` source and build it using the following commands.
```
git clone git://git.osmocom.org/rtl-sdr.git
cd rtl-sdr/
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig
```
Disable the DVB-T driver from loading at boot by adding the device to the ```raspi-blacklist.conf``` file.
```
sudo bash -c 'echo -e "\n# for RTL-SDR:\nblacklist dvb_usb_rtl28xxu\n" >> /etc/modprobe.d/raspi-blacklist.conf'
```
Reboot the system. 
```
sudo reboot
```  
Once the system reloads, test the ```RTL-SDR```.
```
sudo rtl_test
```
My output was:
```
Found 1 device(s):
  0:  Generic, RTL2832U, SN: 77771111153705700

Using device 0: Generic RTL2832U
Found Rafael Micro R820T tuner
Supported gain values (29): 0.0 0.9 1.4 2.7 3.7 7.7 8.7 12.5 14.4 15.7 16.6 19.7 20.7 22.9 25.4 28.0 29.7 32.8 33.8 36.4 37.2 38.6 40.2 42.1 43.4 43.9 44.5 48.0 49.6
[R82XX] PLL not locked!
Sampling at 2048000 S/s.

Info: This tool will continuously read from the device, and report if
samples get lost. If you observe no further output, everything is fine.

Reading samples in async mode...
```
You should receive a similar output message. If there are no errors,  you can end the program with.
```
<CTRL>-C
```
```RTL-SDR``` is now installed and tested on your system. You may now use it with the rest of the software in this guide.

### RTLAMR
[RTLAMR](http://bemasher.github.io/rtlamr/) is ```RTL-SDR``` receiver for Itron ERT compatible smart meters operating in the 900MHz ISM band. 

#### Installation
Set the GO Path and download ```RTLARM```.  
```
export GOPATH=$HOME/go
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
go get github.com/bemasher/rtlamr
```
Try out ```RTL-SDR``` and ```RTLAMR``` together. Run:  
```
sudo rtl_tcp
```
Open a second terminal window and run:  
```
/home/pi/go/bin/rtlamr
```  
You should see meter readings popping up in the new terminal. If you do, it's working!  
  
Exit ```rtlamr``` and ```rtl_tcp``` from the two terminal windows with:
```
<CTRL>-C
```

### Meter Logging
This set of code was created specifically for using ```RTL-SDR``` and ```RTLARM``` to save a new meter reading to a log file at an pre-defined time interval. Due to the limited resources of a Raspberry Pi, it was designed to start the ```RTL_TCP``` service, run ```RTLAMR``` once to look for your intended **Meter ID**, append it to a log file, and close ```RTL_TCP```. 

#### 
Now, let's clone the **EECE 7364** git repo.
```
git clone https://github.com/fentonEECE7364/eece7364.git
```
Move some files around and clean up the rest.
```
mv go/bin/rtlamr eece7364/
rm -rf go/ rtl-sdr/
```
#### Find Your Meter ID
Finding the Meter ID for your personal smart meter may prove to be the hardest part of the whole tutorial. There are several ways you may go about this, but the first step is to verify that your meter is supported by RTLARM by checking updated list on the github page at [meters.csv](https://github.com/bemasher/rtlamr/blob/master/meters.csv). 

Now go to your physical meter, and take a picture of the front ensuring you can read all the information. It will assist you in these next steps.

Your meter should look something similar to the image below. All meters are slightly different, but the ID for my meter is within the red box, with the numbers removed for security reasons.  
  
![Meter ID example](http://i.imgur.com/1YksWbd.png)  
  
Start up ```rtl_tcp``` again:
```
rtl_tcp
```
In a second terminal window, run:
```
/home/pi/eece7364/rtlamr | tee -a /home/pi/eece7364/output.txt
```
Let this run for a few minutes. The output is not only being streamed in the terminal window, but is also being saved to the ```output.txt``` file. Each reading should look similar to this:
```
{Time:2016-04-09T20:37:44.994 SCM:{ID: ######## Type: 4 Tamper:{Phy:00 Enc:01} Consumption:   28994 CRC:0xFE5B}}
```
Where ```ID: ########``` is the Meter ID, and ```Consumption: 28994``` is the energy consumption. Note in some cases, this consumption is not in kWh and the decimal is shifted a few digits. My meter does not give any decimal precision and actually refers to 28994 kWH, but in other others may show 289.94 kWh or something else entirely. This is completely meter specific, and you may need to reference your bill to determine the decimal precision. 

Exit ```rtlamr``` and ```rtl_tcp``` from the two terminal windows with:
```
<CTRL>-C
```

Open the .txt with your preferred file editor. I prefer nano:
```
nano /home/pi/eece7364/output.txt
```
Look through all the meter readings and try to find your **Meter ID**. If you are having trouble, you may also match up the kWh reading on the front of your physical display.

Once you are able to find your **Meter ID**, place this number in the ```info.json``` file, replacing the ```########``` with your ID.
```
nano /home/pi/eece7364/info.json
```

From here, run the bash script that calls  ```RTL_TCP```, ```RTLAMR```, and the python parsing script ```energy_parse.py```.
```
sudo /home/pi/eece7364/meter_read.sh
```
Address any errors that occur. If there are no errors, check the log file to see if a new reading was saved. The log file named by the current month, and is located in:
```
/home/pi/eece7364/logs/
```
If a new entry (or first entry) was added, the energy parsing is working properly! 

#### Cronjob Entry
To create a database of readings over time, we need to create a schedule of meter logging. Edit the system's cronjob to run the scripts at a pre-determined time interval. I've found every 15 minutes to be sufficient.
```
sudo crontab -e
```
Add the following line so the script runs on it own. In the code below, the 15 means it will run every 15 minutes. It also saves the output to ```meter_read.log```. This may be useful in diagnosing a problem if things stop working properly.

```
*/15 * * * * /home/pi/eece7364/meter_read.sh > /home/pi/eece7364/meter_read.log 2>&1
```
Note that it runs on the 15 minute marks of the hour (for example during the 2 o'clock hour, it runs at 2:00, 2:15, 2:30 and 2:45).  

Wait until the next cronjob runs, and verify a new reading was correctly added to the log file.

#### Viewing the Data
After you have saved several readings, you may now start to view the data you have collected. Run the ```plot_kWh.py``` python script:
```
python /home/pi/eece7364/plot_kWh.py
```
This will create a file called ```meter_readings.png``` in the ```eece7364``` directory. If you are using a keyboard and monitor with your Raspberry Pi, you may view the plot directly. If you used ssh to access the device, you will need to transfer this file to your host computer. The easiest method is most likely [scp](https://en.wikipedia.org/wiki/Secure_copy). Your plot should look similar to this:
  
![Meter ID example](http://i.imgur.com/FuCfJmy.png)  
  
Now it is up to you to expand on this data analysis!

## Sources
* http://sdr.osmocom.org/trac/wiki/rtl-sdr
* http://bemasher.github.io/rtlamr/
* http://blog.sdr.hu/2015/06/30/quick-setup-openwebrx.html
* http://matplotlib.org/examples/pylab_examples/plotfile_demo.html
* https://stedolan.github.io/jq/
