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

GPIO.setmode(GPIO.BCM)
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
CENTER_TOLERANCE = 0.2


def setup_rf():
    print("Starting radio...")
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

def import_image():
    main_picture = cv2.imread("images/kayak6.jpg")
    main_picture = cv2.cvtColor(main_picture, cv2.COLOR_BGR2RGB)
    hsv_picture = cv2.cvtColor(main_picture, cv2.COLOR_RGB2HSV)
    
    lower_color = (61, 247, 247)
    upper_color = (180, 255, 255)

    mask = cv2.inRange(hsv_picture, lower_color, upper_color)
    result = cv2.bitwise_and(main_picture, main_picture, mask=mask)
    
    return result, main_picture.shape[1]

setup_rf()

result, picture_width = import_image() 

box_size_row = [0]
box_top_corner = [0,0]
new_line = False

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

actual_box_width = 0
for i in range(len(box_size_row)):
    actual_box_width+=box_size_row[i]

actual_box_width/=(len(box_size_row)-1)

message = list(side_selection(box_top_corner[0], picture_width, actual_box_width))

while len(message) < 32:
    message.append(0)

for i in range(0, 10):
    start = time.time()
    radio.write(message)
    print("Sent the message [" + str(i+1) + "]...")
    time.sleep(1/10)

GPIO.cleanup()