# Importing imaging libraries
import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import numpy as np

# Importing NRF libraries
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

# Setting GPIO mode and intializing the comm pipeline
GPIO.setmode(GPIO.BCM)
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())

# Function to setup RF
def setup_rf():
    radio.begin(0, 17)
    radio.setPayloadSize(32)
    radio.setChannel(0x76)
    radio.setDataRate(NRF24.BR_1MBPS)
    radio.setPALevel(NRF24.PA_MIN)

    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()

    radio.openWritingPipe(pipes[0])
    radio.printDetails()

# Function to select which side, if any, the kayak is on
def side_selection(corner_x, image_width, box_size):
    box_center = corner_x + box_size/2
    print(box_center)
    print(corner_x)
    print(box_size)
    print(image_width)
    
    if(box_center < (image_width*0.4)):
        print("LEFT")
        return "LEFT"
    elif(box_center > (image_width*0.6)):
        print("RIGHT")
        return "RIGHT"
    else:
        print("CENTERED")
        return "CENTERED"

# Test function to cycle through a group of images
def import_image(iteration):
    main_picture = cv2.imread("images/kayak" + str(iteration) + ".jpg")
    main_picture = cv2.cvtColor(main_picture, cv2.COLOR_BGR2RGB)
    hsv_picture = cv2.cvtColor(main_picture, cv2.COLOR_RGB2HSV)
    
    lower_color = (61, 247, 247)
    upper_color = (180, 255, 255)

    mask = cv2.inRange(hsv_picture, lower_color, upper_color)
    result = cv2.bitwise_and(main_picture, main_picture, mask=mask)
    
    return result, main_picture.shape[1]


#### MAIN CODE ####

# Calling setup function
setup_rf()

# Test use to cycle through 6 images
for i in range(1, 7):
    # Calling function to take in the image and its width
    result, picture_width = import_image(i) 

    box_size_row = [0]
    box_top_corner = [0,0]
    new_line = False

    # Determine the location of the top corner of the box and the
    # length of the box
    for y in range(len(result)):
        number_of_instances = 0
        for x in range(len(result[y])):
            if(result[y][x][1] >= 250):
                number_of_instances+=1
                if not new_line:
                    box_top_corner[0] = x; box_top_corner[1] = y;
                new_line = True
        if new_line:
            box_size_row.append(number_of_instances)
            new_line = False
            break

    # Averaging out the different box widths to find a more accurate
    # representation of the width of the box
    actual_box_width = 0
    for i in range(len(box_size_row)):
        actual_box_width+=box_size_row[i]

    actual_box_width/=(len(box_size_row)-1)

    # Creating message to be sent via the nRF to the "vibrators" by
    # calling the side_selection function
    message = list(side_selection(box_top_corner[0], picture_width, actual_box_width))

    # Appending 0s to the end of the string to ensure that 
    while len(message) < 32:
        message.append(0)

    # Sending the message 10 times to ensure that the end devices
    # get the message
    for i in range(0, 10):
        start = time.time()
        radio.write(message)
        print("Sent the message: {}".format(message))
        time.sleep(1/10)

GPIO.cleanup()