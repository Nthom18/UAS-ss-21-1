from datetime import datetime
import os
import time
import picamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)

index = 0
channel = 17

# Create new folder
path = '/home/pi/images'
directory_contents = os.listdir(path)

for i in range(0, len(directory_contents)):
    directory_contents[i] = int(directory_contents[i])

pre_index = 0
folder = '1'
if(len(directory_contents) > 0):
    pre_index = max(directory_contents)
    folder = str(pre_index + 1)

path = os.path.join(path, folder)
os.mkdir(path)


with picamera.PiCamera() as camera:
    # camera.resolution = (2592, 1944) # RPI Cam 1
    camera.resolution = (3280, 2464) # RPI Cam 2


    # forever loop
    while True:
        GPIO.wait_for_edge(channel, GPIO.RISING)

        print("start saving images")
        
        while True:
            start = time.time()

            camera.capture("/home/pi/images/" + folder + "/img_{}.jpg".format(str(index).zfill(6)))
            print("Saved image as img_{}.jpg".format(str(index).zfill(6)))

            while((time.time() - start) < 1): os.wait
            index += 1

            if GPIO.input(channel) == GPIO.LOW:
                break	

        print("stop saving images")
