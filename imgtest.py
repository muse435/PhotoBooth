#!/usr/bin/python
import RPi.GPIO as GPIO, sys, time, os, subprocess, pygame

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO
# Swithes
SWITCH = 26 # button to initiate photos
GPIO.setup(SWITCH,GPIO.IN, pull_up_down=GPIO.PUD_UP)
RESET = 25 #Button to reset
GPIO.setup(RESET,GPIO.IN, pull_up_down=GPIO.PUD_UP) # Terminate

# LEDs
POSE_LED = 12 #Red
GPIO.setup(POSE_LED, GPIO.OUT)
GPIO.output(POSE_LED, False)
PRINT_LED = 21 #Yellow
GPIO.setup(PRINT_LED, GPIO.OUT)
GPIO.output(PRINT_LED, False)
READY_LED = 18 #Green
GPIO.setup(READY_LED, GPIO.OUT)
GPIO.output(READY_LED, True)


# Variables
dir = "/home/pi/PB_archive/"
temp = "home/pi/Pictures/temp.jpg"
width = 768
height = 1024
wid2 = width/2
high2 = height/2
poser = ["First Pose", "Second Pose", "Third Pose", "Last Pose!"]

# pygame
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
pygame.init()
pygame.display.init()
bigfont = pygame.font.SysFont("freeserif",300)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

allpics = os.listdir(dir)
image_count = len(allpics)
for file in allpics:
    print file

def GetDirectory(list):
    list = os.listdir(dir)
    for file in list:
        print file

# TODO: Work on screen layout
def BigNumber(number):
    backGroundCenterSurface = pygame.Surface((width,height))
    backGroundCenterSurface.fill(black)
    screen.blit(backGroundCenterSurface,(0,0))
    backGroundCenterSurface.set_alpha(25)
    screen.blit(bigfont.render(number, 1, white),(200,0))
    pygame.display.update()


def DrawCenterMessage(message,x,y,ss):
    ww = 0.3*ss*len(message)
    hh = ss
    xx = x-ww
    yy = y
    backGroundCenterSurface = pygame.Surface((width,height))
    backGroundCenterSurface.fill(black)
    megafont = pygame.font.SysFont("freeserif",ss,bold = 1)
    screen.blit(backGroundCenterSurface,(0,0))
    screen.blit(megafont.render(message, 1, white),(xx+10,yy+10))
    pygame.display.update()


def DrawCenterMessage2(message,x,y,ss):
    megafont = pygame.font.SysFont("freeserif",ss,bold = 1)
    letsurf = megafont.render(message, 1, white)
    ww = letsurf.get_width()
    hh = letsurf.get_height()
    BGSurface = pygame.Surface((ww+10,hh+10))
    BGSurface.fill(black)
    BGSurfaceblit(letsurf,(5,5))
    screen.blit(BGSurface,(x-ww/2-5,y-hh/2-5))
    pygame.display.update()
    
def DrawCenterPhoto(pose,x,y,ss):
    #ww = 0.3*ss*len(message)
    hh = ss
    #xx = x-ww
    xx = x
    yy = y
    backGroundCenterSurface = pygame.Surface((width,height))
    backGroundCenterSurface.fill(black)
    megafont = pygame.font.SysFont("freeserif",ss,bold = 1)
    screen.blit(backGroundCenterSurface,(0,0))
    screen.blit(megafont.render(pose, 1, white),(1,1))
    photo = pygame.image.load(temp)
    photo = pygame.scale(photo, (wid2, high2))
    screen.blit(photo,(0,0))
    pygame.display.update()    

def terminate(Terminated):
    GPIO.cleanup()
    pygame.display.quit
    pygame.quit()
    sys.exit(Terminated)

# TODO: Impliment
def checkForKeyPress(): 
    for event in pygame.event.get():
        if event.key == K_ESCAPE:
            terminate("Esc button pushed")
        else:
            return None
        

DrawCenterMessage("Push The Button", wid2, high2, 70)

while True:
    if GPIO.input(RESET) == False:
        terminate("Killed by Reset Switch")
    if GPIO.input(SWITCH) == False:
        DrawCenterPhoto("1", wid2, high2, 20)
        time.sleep(20)
        terminate("End of test")
