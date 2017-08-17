# GatherCiscoRunningConfig
Grabs configuration of Cisco devices via SSH

Dependencies: netmiko, python standard library
add list of devices to backup to deviceList, seperated by new line 

Usage:
pip install netmiko
python gatherRunning.py


gatherRunning will iterate through the device list, scan for port 22, connect if it is open and save the config under configs directory
