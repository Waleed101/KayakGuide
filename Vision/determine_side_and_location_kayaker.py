import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import numpy as np

pic_2 = cv2.imread("kayaker2.jpg")
pic = cv2.cvtColor(pic_2, cv2.COLOR_BGR2RGB)
hsv_pic = cv2.cvtColor(pic_2, cv2.COLOR_RGB2HSV)

while True:
    cv2.imshow('Main', pic_2)
    cv2.imshow('RGB', pic)
    cv2.imshow('HSV', hsv_pic)
    if(cv2.waitKey(1) == 27):
        break

cv2.destroyAllWindows()

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
                print("Found at (" + str(x) + ", " + str(y) + ")")
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
    print("RIGHT")
else:
    print("LEFT")

