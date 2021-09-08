#!/bin/bash

geany
cd ~/Software/Masterarbeit
lxterminal --command="python3 start.py 2>&1 | tee log.txt" &
sudo barrier & 

# bash /home/pi/Software/Masterarbeit/start.sh
