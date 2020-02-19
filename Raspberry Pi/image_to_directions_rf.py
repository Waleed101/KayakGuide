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


pic = cv2.imread("kayaker3.jpg")
pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
hsv_pic = cv2.cvtColor(pic, cv2.COLOR_RGB2HSV)

light = (61, 247, 247)
dark = (180, 255, 255)

mask = cv2.inRange(hsv_pic, light, dark)
result = cv2.bitwise_and(pic, pic, mask=mask)

sizeOfBox = [0]
targLoc = [0,0]
newLine = False

for y in range(len(result)):
    sizeCount = 0
    for x in range(len(result[y])):
        if(result[y][x][1] >= 250):
            sizeCount+=1
            if not newLine:
                targLoc[0] = x; targLoc[1] = y;
            newLine = True
    if newLine:
        sizeOfBox.append(sizeCount)
        newLine = False
        break

width = 0
for i in range(len(sizeOfBox)):
    width+=sizeOfBox[i]

width/=(len(sizeOfBox)-1)
print(sizeOfBox)
print(targLoc)
print(width)

if(targLoc[0] > pic.shape[0]/2):
    message = list("RIGHT")
    print("RIGHT")
else:
    message = list("LEFT")
    print("RIGHT")
    
while len(message) < 32:
    message.append(0)

while True:
    start = time.time()
    radio.write(message)
    print("Sent the message: {}".format(message))
    time.sleep(1)
    if cv2.waitKey(1) == 27:
        break

GPIO.cleanup()