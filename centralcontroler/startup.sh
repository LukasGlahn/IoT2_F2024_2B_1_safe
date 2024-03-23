#!/bin/sh
cd /home/lukasglahn/Desktop/Iot2/
pwd
screen -S ping -dm bash -c 'ping -i 15 1.1.1.1'
screen -S main -dm bash -c 'python main.py'
screen -S backup -dm bash -c 'python backup.py'
screen -ls