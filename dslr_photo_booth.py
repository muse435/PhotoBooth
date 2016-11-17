#!/usr/bin/python
import RPi.GPIO as GPIO, sys, time, os, subprocess, pygame, thread, shutil, random


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
stripDir = "/home/pi/photobooth_images/strip_archive/"
snapShotDir = "/home/pi/photobooth_images/snap/"
snapShotArchive = "/home/pi/photobooth_images/snap_archive/"
montageDir = "/home/pi/photobooth_images/montage/"
lastStrip = "/home/pi/photobooth_images/default/tempStrip.jpg"
stripLabel = "/home/pi/photobooth_images/default/photobooth_label.jpg"
ready = False
width = 768
height = 1024
wid2 = width/2
high2 = height/2
poser = ["First Pose", "Second Pose", "Third Pose", "Last Pose!"]
timerLength = 1
# geometry = "968x648"
geometry = "484x324"

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
    RemoveTempFiles()
    GPIO.cleanup()
    pygame.display.quit
    pygame.quit()
    sys.exit(Terminated)

def AssembleAndSave(geometry, printStrip): #TODO: did i do this corectly?
    global stripDir     # Why did you redeclare all these as global?
    global snapShotDir  # Is it really neccesary or were you just trying things?
    global montageDir   # If not, re-test after removing them
    global lastStrip
    
    # copy original single photos to a backup folder
    src_files = os.listdir(snapShotDir)
    for item in src_files:
        full_file_name = os.path.join(snapShotDir, item)
        print(full_file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy2(full_file_name, snapShotArchive)

    # resize the images for the strip
    subprocess.call("mogrify -resize " + geometry + " " + snapShotDir + "*.jpg", shell=True)
    # montage them into a photo strip
    subprocess.call("montage " + snapShotDir + "*.jpg -tile 1x4 -geometry +1+1 " + montageDir + "temp_montage2.jpg", shell=True)
    subprocess.call("montage " + montageDir + "temp_montage2.jpg " + stripLabel + " -tile 1x2 -geometry +1+1 " + montageDir + "temp_montage3.jpg", shell=True)
    # copy the photo strips to a backup folder
    suffix = time.strftime("%Y%m%d%H%M%S")
    shutil.copyfile(montageDir + "temp_montage3.jpg", stripDir + "PB_" + suffix + ".jpg")
    # update lastStrip so we display the correct one
    lastStrip = stripDir + "PB_" + suffix + ".jpg"
    if (printStrip):
        subprocess.call("montage" + montageDir + "temp_montage3.jpg montage" + montageDir + "temp_montage3.jpg -tile 2x1 -geometry +5+5 " + montageDir + "temp_montage4.jpg", shell=True)
        #subprocess.call("lp -d name of printer here " + montageDir + "temp_montage4.jpg", shell=True)
        print("photo now printing")
    RemoveTempFiles()

def RemoveTempFiles():
    deleteAllFilesInFolder(snapShotDir)
    deleteAllFilesInFolder(montageDir)

def deleteAllFilesInFolder(folder):
    # from http://stackoverflow.com/questions/185936/delete-folder-contents-in-python
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def UploadStrip():
    print("Uploading Stip")
    #TODO: find a cloud to upload to
    #TODO: use the API


def SlideShow():
    print("starting the slideshow")
    global ready
    allPics = os.listdir(stripDir)
    random.shuffle(allPics)
    imageCount = len(allPics)
    counter = 0
    if imageCount == 0:
        ready = True
        DrawCenterMessage("Push The Button", wid2, high2, 70)
    imageCount -= 1
    while ready == False:
        stripSlide = allPics[counter]
        DrawStrip("Slide Show", stripDir + allPics[counter])
        print("Slide Show - showing: " + stripDir + allPics[counter])
        time.sleep(3)
        if counter == imageCount:
            counter = 0
        else:
            counter += 1
        
thread.start_new_thread(SlideShow, ())

while True:
    #TODO: run this as a thread so we can kill the program at any point?
    if GPIO.input(RESET) == False:
        terminate("Killed by Reset Switch")
    
    if GPIO.input(SWITCH) == False:
        global ready
        snap = 0
        ready = True
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
            filepath = snapShotDir + time.strftime("%Y%m%d%H%M%S") + ".jpg"
            gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename " + filepath, stderr=subprocess.STDOUT, shell=True)
            print(gpout)

            DrawPose(snap, filepath)
            time.sleep(2)
            if "ERROR" not in gpout:
                snap += 1
        DrawCenterMessage("Assembling" ,wid2,high2+100,100)
        print("Assembling the photo strip")
        
        
        if GPIO.input(PRINT) == True:
            GPIO.output(PRINT_LED, True)
            print("Please wait while your photos print...")
            AssembleAndSave(geometry, True)
            print("Photo Saved")
            DrawStrip("Printing", lastStrip)
            PrintStrip(lastStrip)
            # TODO: determine amount of time to compile the montage, and if printing the photo how long that will take
            # TODO: check status of printer instead of using this arbitrary wait time
            time.sleep(10)
            GPIO.output(PRINT_LED, False)
            
        else:
            print("Please wait while your photos save...")
            AssembleAndSave(geometry, False)
            print("Photo Saved")
            DrawStrip("Saving", lastStrip)
            time.sleep(10)

        RemoveTempFiles()
        print("ready for next round")
        GPIO.output(READY_LED, True)
        thread.start_new_thread(SlideShow, ())

