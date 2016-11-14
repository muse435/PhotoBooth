#!/usr/bin/python
import RPi.GPIO as GPIO, sys, time, os, subprocess, pygame, random, thread

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO
# Swithes
SWITCH = 26 # button to initiate photos
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
RESET = 25 #Button to reset
GPIO.setup(RESET, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Terminate
PRINT = 20 #
GPIO.setup(PRINT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
stripDir = "/home/pi/PB_archive/"
tempStrip = "/home/pi/Pictures/tempStrip.jpg"
width = 768
height = 1024
wid2 = width/2
high2 = height/2
poser = ["First Pose", "Second Pose", "Third Pose", "Last Pose!"]
timerLength = 5

# pygame
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
pygame.init()
pygame.display.init()
bigfont = pygame.font.SysFont("freeserif",500)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def CountDownScreen(pose, timerNumber):
    backGroundCenterSurface = pygame.Surface((width,height))
    backGroundCenterSurface.fill(black)
    screen.blit(backGroundCenterSurface,(0,0))
    backGroundCenterSurface.set_alpha(25)
    screen.blit(bigfont.render(timerNumber, 1, white),(200, 300))
    poseFont = pygame.font.SysFont("freeserif", 80, bold = 1)
    screen.blit(poseFont.render(pose, 1, white),(120,150))
    screen.blit(poseFont.render(pose, 1, white),(120,950))
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
    
def DrawPose(snap, picture):
    #2:3
    backGroundCenterSurface = pygame.Surface((width,height))
    backGroundCenterSurface.fill(black)
    megafont = pygame.font.SysFont("freeserif",75,bold = 5)
    screen.blit(backGroundCenterSurface,(0,0))
    screen.blit(megafont.render(poser[snap], 1, white),(110,150))
    photo = pygame.image.load(picture)
    photo = pygame.transform.scale(photo, (690, 460))
    screen.blit(photo,(0,400))
    pygame.display.update() 

def DrawStrip(message, picture):
    #2:3
    backGroundCenterSurface = pygame.Surface((width,height))
    backGroundCenterSurface.fill(black)
    megafont = pygame.font.SysFont("freeserif",90,bold = 5)
    screen.blit(backGroundCenterSurface,(0,0))
    screen.blit(megafont.render(message, 1, white),(150,50))
    photo = pygame.image.load(picture)
    photo = pygame.transform.scale(photo, (362, 1000))
    screen.blit(photo,(147,200))
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

# Slide show needs to be a thread
def SlideShow(index):
    counter = 0
    global ready
    if index == 0:
        ready = True
        DrawCenterMessage("Push The Button", wid2, high2, 70)
    index -= 1
    while ready == False:
        stripSlide = allpics[counter]
        DrawStrip("Slide Show", stripDir + allpics[counter])
        time.sleep(3)
        #update "ready"
        if counter == index:
            counter = 0
        else:
            counter += 1
        
allpics = os.listdir(stripDir)
random.shuffle(allpics)
imageCount = len(allpics)
ready = False
#creat a thread here
thread.start_new_thread(SlideShow, (imageCount, ))

while True:
    
    if GPIO.input(RESET) == False:
        terminate("Killed by Reset Switch")
    
    if GPIO.input(SWITCH) == False:
        snap = 0
        ready = True
        # TODO: Work on screen layout
        DrawCenterMessage("Get Ready" ,wid2,high2+100,70)
        for i in range(5):
            GPIO.output(READY_LED, False)
            time.sleep(0.5)
            GPIO.output(READY_LED, True)
            time.sleep(0.5)
        GPIO.output(READY_LED, False)
    
        while snap < 4:
            pose_number = snap+1
        
            for i in range(timerLength):
                GPIO.output(POSE_LED, False)
                time.sleep(0.5)
                GPIO.output(POSE_LED, True)
                time.sleep(0.5)
                countdown = str(timerLength-i)
                CountDownScreen(poser[snap], countdown)
            time.sleep(1)
            # TODO: Work on screen layout
            DrawCenterMessage("Snap" ,wid2,high2+100,100)
            # Takes a photo with connected DSLR
            print("pose number %d" % pose_number)
            GPIO.output(POSE_LED, False)
            filepath = "/home/pi/photobooth_images/photobooth" + time.strftime("%Y%m%d%H%M%S") + ".jpg" # inject a timestamp into the filename
            gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename " + filepath, stderr=subprocess.STDOUT, shell=True)
            print(gpout)

            DrawPose(snap, filepath)
            time.sleep(2)
            if "ERROR" not in gpout:
                snap += 1
        # Create photo strip and send it to the printer
        # TODO: Work on screen layout
        DrawCenterMessage("Assembling" ,wid2,high2+100,100)
        print("Assembling the photo strip")
        
        
        if GPIO.input(PRINT) == True:
            GPIO.output(PRINT_LED, True)
            subprocess.call("sudo /home/pi/scripts/PhotoBooth/assemble_and_print", shell=True)
            print("Please wait while your photos print...")
            allpics = os.listdir(stripDir)
            random.shuffle(allpics)
            imageCount = len(allpics)
            DrawStrip("Printing", stripDir + allpics[imageCount-1])
            # TODO: determine amount of time to compile the montage, and if printing the photo how long that will take
            # TODO: check status of printer instead of using this arbitrary wait time
            time.sleep(10)
            GPIO.output(PRINT_LED, False)
            
        else:
            subprocess.call("sudo /home/pi/scripts/PhotoBooth/assemble_and_save", shell=True)
            # TODO: display photo strip and printing
            print("Please wait while your photos save...")
            allpics = os.listdir(stripDir)
            random.shuffle(allpics)
            imageCount = len(allpics)
            DrawStrip("Saving", stripDir + allpics[imageCount-1])
            time.sleep(10)
        
        print("ready for next round")
        GPIO.output(READY_LED, True)
        random.shuffle(allpics)
        thread.start_new_thread(SlideShow, (imageCount, ))
