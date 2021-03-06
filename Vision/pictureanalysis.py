import cv2
import numpy as np

## Read
img = cv2.imread("kayaking.jpg")
cv2.show()

## convert to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask1 = cv2.inRange(hsv, (25, 255, 255), (40, 255, 255))

## mask o yellow (15,0,0) ~ (36, 255, 255)
# mask2 = cv2.inRange(hsv, (15,0,0), (36, 255, 255))

## final mask and masked
# mask = cv2.bitwise_or(mask1, mask2)
target = cv2.bitwise_and(img,img, mask=mask1)

cv2.imwrite("target.jpg", target)