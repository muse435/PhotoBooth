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
screenWidth = 900
screenHeight = 1440
poser = ["First Pose", "Second Pose", "Third Pose", "Last Pose!"]
timerLength = 5
snapGeometry = "1936x1296"
labelGeometry = "1936x194"
#snapGeometry = "968x648"
#labelGeometry = "968x97"
#snapGeometry = "484x324"
#labelGeometry = "484x49"

# pygame
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def CountDownScreen(pose, timerNumber):
    backGroundCenterSurface = pygame.Surface((screenWidth,screenHeight))
    backGroundCenterSurface.fill(black)
    screen.blit(backGroundCenterSurface,(0,0))
    bigfont = pygame.font.SysFont("freeserif",1000)
    screen.blit(bigfont.render(timerNumber, 1, white),(200, 200))
    poseFontSize = 170
    centerFont = screenWidth - len(pose) * poseFontSize * .48
    poseFont = pygame.font.SysFont("freeserif", poseFontSize, bold = 1)
    screen.blit(poseFont.render(pose, 1, white),(centerFont,20))
    screen.blit(poseFont.render(pose, 1, white),(centerFont,1230))
    pygame.display.update()

def DrawCenterMessage(message,x,y,ss):
    backGroundCenterSurface = pygame.Surface((screenWidth,screenHeight))
    backGroundCenterSurface.fill(black)
    megafont = pygame.font.SysFont("freeserif",ss,bold = 1)
    screen.blit(backGroundCenterSurface,(0,0))
    screen.blit(megafont.render(message, 1, white),(x,y))
    pygame.display.update()

def DrawPose(pose, picture):
    backGroundCenterSurface = pygame.Surface((screenWidth,screenHeight))
    backGroundCenterSurface.fill(black)
    photo = pygame.image.load(picture)
    photo = pygame.transform.scale(photo, (880, 587))
    screen.blit(photo,(10,440))
    poseFontSize = 170
    centerFont = screenWidth - len(pose) * poseFontSize * .48
    poseFont = pygame.font.SysFont("freeserif", poseFontSize, bold = 1)
    screen.blit(poseFont.render(pose, 1, white),(centerFont,20))
    screen.blit(poseFont.render(pose, 1, white),(centerFont,1230))
    pygame.display.update() 

def DrawStrip(message, picture):
    backGroundCenterSurface = pygame.Surface((screenWidth,screenHeight))
    backGroundCenterSurface.fill(black)
    screen.blit(backGroundCenterSurface,(0,0))
    messageFontSize = 90
    centerFont = screenWidth - len(message) * messageFontSize * .6
    megafont = pygame.font.SysFont("freeserif", messageFontSize, bold = 5)
    screen.blit(megafont.render(message, 1, white),(centerFont,50))
    photo = pygame.image.load(picture)
    photo = pygame.transform.scale(photo, (434, 1200))
    screen.blit(photo,(240,200))
    pygame.display.update() 
    
def terminate(Terminated):
    RemoveTempFiles()
    GPIO.cleanup()
    pygame.display.quit
    pygame.quit()
    sys.exit(Terminated)

def AssembleAndSave(geometry, lableGeo): #TODO: did i do this corectly?
    global stripDir     # Why did you redeclare all these as global?
    global snapShotDir  # Is it really neccesary or were you just trying things?
    global montageDir   # If not, re-test after removing them
    global lastStrip

    DrawCenterMessage("Assembling Strip" ,10 ,620, 120)
    print("Assembling the photo strip")

    # copy original single photos to a backup folder
    src_files = os.listdir(snapShotDir)
    for item in src_files:
        full_file_name = os.path.join(snapShotDir, item)
        print(full_file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy2(full_file_name, snapShotArchive)

    # resize the images for the strip
    subprocess.call("mogrify -resize " + geometry + " " + snapShotDir + "*.jpg", shell=True)
    subprocess.call("mogrify -resize " + lableGeo + " " + stripLabel, shell=True)
    # montage them into a photo strip
    subprocess.call("montage " + snapShotDir + "*.jpg -tile 1x4 -geometry +1+1 " + montageDir + "temp_montage2.jpg", shell=True)
    subprocess.call("montage " + montageDir + "temp_montage2.jpg " + stripLabel + " -tile 1x2 -geometry +1+1 " + montageDir + "temp_montage3.jpg", shell=True)
    # copy the photo strips to a backup folder
    suffix = time.strftime("%Y%m%d%H%M%S")
    shutil.copyfile(montageDir + "temp_montage3.jpg", stripDir + "PB_" + suffix + ".jpg")
    print("Photo Saved")
    # update lastStrip so we display the correct one
    lastStrip = stripDir + "PB_" + suffix + ".jpg"
    if (GPIO.input(PRINT) == True):
        DrawStrip("         Printing", lastStrip)
        subprocess.call("montage " + montageDir + "temp_montage3.jpg " + montageDir + "temp_montage3.jpg -tile 2x1 -geometry +5+5 " + montageDir + "temp_montage4.jpg", shell=True)
        GPIO.output(PRINT_LED, True)
        print("photo now printing")
        #subprocess.call("lp -d name of printer here " + montageDir + "temp_montage4.jpg", shell=True)
        # TODO: determine amount of time to compile the montage, and if printing the photo how long that will take
        # TODO: check status of printer instead of using this arbitrary wait time
        time.sleep(10)
        GPIO.output(PRINT_LED, False)       
    else:
        DrawStrip("             Saving", lastStrip)
        time.sleep(10)
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
    imageCount = len(allPics)    
    random.shuffle(allPics)
    counter = 0
    if imageCount == 0:
        ready = True
        DrawCenterMessage("Push The Button", 10, 650, 122)
    imageCount -= 1
    GPIO.output(READY_LED, True)
    while ready == False:
        stripSlide = allPics[counter]
        DrawStrip("Ready to Start", stripDir + allPics[counter])
        time.sleep(3)
        if counter == imageCount:
            counter = 0
            random.shuffle(allPics)
        else:
            counter += 1
        
thread.start_new_thread(SlideShow, ())

while True:
    #TODO: run this as a thread so we can kill the program at any point?
    if GPIO.input(RESET) == False:
        terminate("Killed by Reset Switch")
    
    if GPIO.input(SWITCH) == False:
        snap = 0
        ready = True
        DrawCenterMessage("Get Ready", 10, 620, 197)
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
            DrawCenterMessage("Snap!" , 0, 500, 370)
            # Takes a photo with connected DSLR
            print("pose number %d" % pose_number)
            GPIO.output(POSE_LED, False)
            filepath = snapShotDir + time.strftime("%Y%m%d%H%M%S") + ".jpg"
            gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename " + filepath, stderr=subprocess.STDOUT, shell=True)
            print(gpout)
            DrawPose(poser[snap], filepath)
            time.sleep(2)
            if "ERROR" not in gpout:
                snap += 1
        
        AssembleAndSave(snapGeometry, labelGeometry)
        ready = False
        print("ready for next round")
        thread.start_new_thread(SlideShow, ())
        
