#!/usr/bin/python

import RPi.GPIO as GPIO, time, os, subprocess, sys

#TODO: GPIO setup

while True:
  #TODO: switch 1 to button input
  if (1):
    snap = 0
    #TODO: Turn off Button LED 
    while snap <4:
      #Turn on Pose LED and gives time to strike a pose
      print("pose!")
      #TODO: Turn on pose LED
      snap += 1
      #TODO: change pose time
      time.sleep(.1)
      #Takes a photo with connected DSLR
      print("SNAP=%d" %snap)
      gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename /home/pi/photobooth_images/photobooth%Y%m%d%H%M%S.jpg", stderr=subprocess.STDOUT, shell=True)
      print(gpout)
      #TODO: Turn off pose LED
      #TODO: Turn on wait  LED
      #TODO: Change wait time
      time.sleep(1)
      #TODO: Turn off wait button
    #calls another script to create the strip and send it to the printer
    print("please wait while your photos print...")
    subprocess.call("sudo /home/pi/scripts/photobooth_tester/assemble_and_print", shell=True)
    #TODO: turn on Print LED
    #determine amount of time to compile the montage, and if printing the photo how long that will take
    time.sleep(10)
    #TODO: Turn off print LED
    print("ready for next round")
    
    
    # this needs to be removed for the final 
    sys.exit("End of Test")
    

