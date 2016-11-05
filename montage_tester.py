#!/usr/bin/python

import time, os, subprocess, sys

while True:
  if (1):
    snap = 0
    print("please wait while we build your photo strip")

    subprocess.call("sudo /home/pi/scripts/photobooth_tester/assemble_and_print_hi_res", shell=True)
    sys.exit("End of Test")
    

