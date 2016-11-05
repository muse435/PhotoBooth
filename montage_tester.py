#!/usr/bin/python

#this is a simple script to test different photostrip montagaes

import subprocess, sys

while True:
    print("please wait while we build your photo strip")
    subprocess.call("sudo /home/pi/scripts/photobooth_tester/assemble_and_print_hi_res", shell=True)
    sys.exit("End of Test")
    

