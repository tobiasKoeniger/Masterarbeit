#!/bin/bash

# This bash file is run after the window manager has started. 
# The auto start entry is situated here: 
# sudo gedit /etc/xdg/lxsession/LXDE-pi/autostart

# Move into software directory
cd ~/Software/Masterarbeit

# Open terminal and run hydroponics software. 
# Output from program is printed in the terminal 
# as well as saved in the log.txt file.
lxterminal --command="python3 start.py 2>&1 | tee log.txt" &

# Run barrier to share the mouse and keyboard with another pc.
sudo barrier & 

# Run the dev environment
geany

# Command to test this file:
# bash /home/pi/Software/Masterarbeit/start.sh
