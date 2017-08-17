#!/usr/bin/python
from netmiko import ConnectHandler
from datetime import datetime
import socket, os, sys
from getpass import getpass


# list of devices to backup
with open('deviceList') as f:
        devices = f.read().splitlines()

# check for device config dir -- create it if it isn't there
if not os.path.exists('configs'):
        os.makedirs('configs')

# gathers current time and formats it to append to filename
def getTime():
        time = str(datetime.now())
        time = time[0:16]
        time = time.replace(' ','_')
        return time


def main():
        userInput = raw_input("Devices in 'deviceList' will be backed up over ssh. (y/n) ").lower()
        if userInput == 'y':
                pass
        else:
                exit()
        username = raw_input("Username: ")
        password = getpass("Password: ")

        x = 0
        for each in devices:

                time=getTime()
                # check if ssh is open, if not, go to next device
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((devices[x], 22))

                if result == 0:
                        print "Port 22 is open on device " + devices[x] + ". Attempting to connect over SSH"
                        try:
                                cisco = {
                                'device_type':'cisco_ios',
                                'ip':devices[x],
                                'username':username,
                                'password':password,
                                }

                                net_connect=ConnectHandler(**cisco)

                                        # set term to 0 so show run output is whole
                                net_connect.send_command("term length 0")
                                running = net_connect.send_command("show running")

                                        # set filename to device hostname and date/time
                                fileName = net_connect.send_command("show running | inc hostname").split()[1] + "_" + time

                                        # open file for writing and save the running config variable to it
                                f = open('configs/'+fileName, 'w')
                                f.write(running)
                                f.close()

                                        # append success message to log
                                successMessage = time + " successfully backed up device at IP: " + devices[x] + "\n"
                                log = open('log.txt', 'a')
                                log.write(str(successMessage))
                                log.close()
                                print successMessage
                                print "Connected to " + str(x + 1) + " devices so far, with " + str((len(devices) - x)) + " left to backup\n"
                        except:

                                        # catch errors and write an error message to log.txt when they happen
                                errorMessage = time + " unable to reach device at IP: " + devices[x] + "\n"
                                log = open('log.txt', 'a')
                                log.write(str(errorMessage))
                                log.close()
                                print errorMessage
                else:
                        print "port 22 is not open"
                        print "result is " + str(result)
                x += 1

main()
