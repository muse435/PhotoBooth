#!/usr/bin/python
import RPi.GPIO as GPIO, sys, time, os, subprocess, pygame, picamera

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#LEDs
#Yellow
PRINT_LED = 21
GPIO.setup(PRINT_LED, GPIO.OUT)
GPIO.output(PRINT_LED, False)
#Red
POSE_LED = 12
GPIO.setup(POSE_LED, GPIO.OUT)
GPIO.output(POSE_LED, False)
#Green
BUTTON_LED = 18
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.output(BUTTON_LED, True)

#Switches
SWITCH = 26
GPIO.setup(SWITCH, GPIO.IN)
#not yet implimented
PRINT_SWITCH=14
GPIO.setup(PRINT_SWITCH, GPIO.IN)
RESET = 25
GPIO.setup(RESET, GPIO.IN)

# variables
poser=["First Pose","Number two","Third time","last Pose!"]
width = 1024
wide = 1024
wid2 = width/2
height = 768
high = 768
high2 = height/2
continue_loop = True
current_image = 0
camera = picamera.PiCamera()
camera.preview_alpha = 128
waitforit = 200
counter=waitforit
dir = "/home/pi/PB_archive/"
allpics = os.listdir(dir)
image_count = len(allpics)
for file in allpics:
  print file

#pygame stuff
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
pygame.init()
pygame.display.init()
bigfont=pygame.font.SysFont("freeserif",300)
#screen = pygame.display.set_mode((width,height),pygame.FULLSCREEN)#FULLSCREEN
def GetDirectory(list):
#get directory contents for /home/pi/PB_archive/
list = os.listdir(dir)

for file in list:
  print file
    def BigNumber(number):
      backgroundCenterSurface = pygame.Surface((width,height))
      backgroundCenterSurface.fill(black)
      screen.blit(backgroundCenterSurface,(0,0))
      backgroundCenterSurface.set_alpha(25)
      screen.blit(bigfont.render(number, 1, white),(200,0))
      pygame.display.update()
    def DrawCenterMessage(message,x,y,ss):

#displays notification messages onto the screen
ww = 0.4*ss*len(message)
hh = ss
xx = x-ww/2
yy = y-hh/2
backgroundCenterSurface = pygame.Surface((width,height))#size
backgroundCenterSurface.fill(black)
megafont = pygame.font.SysFont("freeserif",ss,bold=1)
screen.blit(backgroundCenterSurface,(0,0))#position
screen.blit(megafont.render(message, 1, white),(xx+10,yy+10))
pygame.display.update()
def DrawCenterMessage2(message,x,y,ss):
megafont = pygame.font.SysFont("freeserif",ss,bold=1)
letsurf = megafont.render(message, 1, white)
ww = letsurf.get_width()
hh = letsurf.get_height()
BGSurface = pygame.Surface((ww+10,hh+10))
BGSurface.fill(black)
BGSurface.blit(letsurf,(5,5))
screen.blit(BGSurface,(x-ww/2-5,y-hh/2-5))
pygame.display.update()
def terminate():
pygame.display.quit
pygame.quit()
sys.exit

# KRT 17/06/2012 rewrite event detection to deal with mouse use
def checkForKeyPress():
for event in pygame.event.get():
if event.type == QUIT: #event is quit
terminate()
elif event.type == KEYDOWN:
if event.key == K_ESCAPE: #event is escape key
terminate()
else:
return event.key #key found return with it
# no quit or key events in queue so return None
return None
DrawCenterMessage("Hit the switch",wid2,high2,100)
while True:
if (GPIO.input(SWITCH)):
  snap = 0
  while snap < 4:
    DrawCenterMessage(poser[snap],wid2,high2+100,100)
    GPIO.output(BUTTON_LED, False)
    GPIO.output(POSE_LED, True)
    time.sleep(1.5)
    camera.start_preview()
    for i in range(5):
      GPIO.output(POSE_LED, False)
      time.sleep(0.5)
      GPIO.output(POSE_LED, True)
      time.sleep(0.5)
      countdown=str(5-i)
      BigNumber(countdown)#,300,300,(wid2-150),(10))
    GPIO.output(POSE_LED, False)
    DrawCenterMessage("SNAP",wid2,high2,100)
    fname = "/home/pi/photobooth_images/photobooth"+str(snap)+".jpg"
    #command = "raspistill -t 1000 -o /home/pi/photobooth_images/photobooth"
    # +str(snap) +".jpg -q 100 -w 1200"
    camera.capture(fname)
    camera.stop_preview()
    freeze=pygame.image.load(fname)
    freeze=pygame.transform.scale(freeze,(width,height))
    screen.blit(freeze,(0,0))
    pygame.display.update()
    #os.system(command)
    #print(command)
    #print(gpout)
    #if "ERROR" not in gpout:
    snap += 1
    GPIO.output(POSE_LED, False)
    time.sleep(2)
    DrawCenterMessage("Please Wait",wid2,high2,100)
    GPIO.output(PRINT_LED, True)

    # build image and send to printer
    if (GPIO.input(14)==0):
      DrawCenterMessage("saving picture",wid2,high2-2,100)
      subprocess.call("sudo /home/pi/scripts/photobooth/assemble_and_save", shell=True)
    else:
      DrawCenterMessage("printing",wid2,high2,100)
      subprocess.call("sudo /home/pi/scripts/photobooth/assemble_and_print", shell=True)
    # TODO: implement a reboot button
    #if event.type == QUIT:
    # pygame.quit()
    # sys.exit()
    # Wait to ensure that print queue doesn't pile up
    # TODO: check status of printer instead of using this arbitrary wait time
    time.sleep(10)
    DrawCenterMessage("Ready",wid2,high2,100)
    GPIO.output(PRINT_LED, False)
    GPIO.output(BUTTON_LED, True)

    #update directory of image files
    allpics=os.listdir(dir)
    image_count = len(allpics)
    #/home/pi/PB_archive/PB_${suffix}.jpg
    else:
      #switch not pressed
      counter -= 1
      time.sleep(.01)
if (GPIO.input(RESET) == 0):
terminate()
if (counter < 1):
counter=waitforit
image = pygame.Surface((width,height))
if (current_image<image_count):
fname=allpics[current_image]
#DrawCenterMessage(fname,400,70,100,350)
magna=pygame.image.load(dir+fname)
magna=pygame.transform.scale(magna,(width,height))
screen.blit(magna,(0,0))
pygame.display.update()
current_image += 1
if (current_image >= image_count):
current_image=0
