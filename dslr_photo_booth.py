#!/usr/bin/python

import RPi.GPIO as GPIO, time, os, subprocess, sys


GPIO.setmode(GPIO.BCM)

SWITCH = 26
GPIO.setup(SWITCH,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#RESET = 25
#GPIO.setup(RESET, GPIO.IN)

#POSE_LED => Red
POSE_LED = 12
GPIO.setup(POSE_LED, GPIO.OUT)
GPIO.output(POSE_LED, False)
#PRINT_LED => Yellow
PRINT_LED = 21
GPIO.setup(PRINT_LED, GPIO.OUT)
GPIO.output(PRINT_LED, False)
#READY_LED => Green
READY_LED = 18
GPIO.setup(READY_LED, GPIO.OUT)
GPIO.output(READY_LED, True)


while True:
  if GPIO.input(SWITCH) == False:
    snap = 0
    for i in range(5):
      GPIO.output(READY_LED, False)
      time.sleep(0.5)
      GPIO.output(READY_LED, True)
      time.sleep(0.5)
    GPIO.output(READY_LED, False)
    while snap <4:      
      print("pose!")
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.5)
        GPIO.output(POSE_LED, True)
        time.sleep(0.5)
      for i in range(10):
        GPIO.output(POSE_LED, False)
        time.sleep(0.1)
        GPIO.output(POSE_LED, True)
        time.sleep(0.1)
      time.sleep(0.7)
      GPIO.output(POSE_LED, True)
      #Takes a photo with connected DSLR
      print("SNAP=%d" %snap)
      GPIO.output(POSE_LED, False)
      gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename /home/pi/photobooth_images/photobooth%Y%m%d%H%M%S.jpg", stderr=subprocess.STDOUT, shell=True)
      print(gpout)
      if "ERROR" not in gpout:
        snap += 1
    #calls another script to create the strip and send it to the printer
    print("Assembling the photo strip")
    GPIO.output(PRINT_LED, True)
    subprocess.call("sudo /home/pi/scripts/photobooth_tester/assemble_and_print", shell=True)
    print("please wait while your photos print...")
    # TODO: determine amount of time to compile the montage, and if printing the photo how long that will take
    # TODO: check status of printer instead of using this arbitrary wait time
    time.sleep(1)
    GPIO.output(PRINT_LED, False)
    print("ready for next round")
    GPIO.output(READY_LED, True)
    #GPIO.cleanup()
    #sys.exit("Exit!")
