import cv2 as cv
import numpy as np

def nothing(x):
    pass

# fobj = open(r"Masked.txt", "w")

# minHSV = np.array([])

lowerHSV = np.array([0,0,0])     
upperHSV = np.array([180,255,255])
frame = cv.imread(r"C:\Users\walee\Desktop\Eng Comps\Western Engineering Competition 2020\programming\python\kayaker.jpg")

# create the Trackbar window to find the appropriate HSV bounds
cv.namedWindow('TrackBARS')
cv.createTrackbar("L-H", "TrackBARS", 0, 180, nothing)  # bounds for Lower Hue
cv.createTrackbar("L-S", "TrackBARS", 0, 255, nothing) # bounds for Lower Saturation
cv.createTrackbar("L-V", "TrackBARS", 0, 255, nothing) # bounds for Lowever Value
cv.createTrackbar("U-H", "TrackBARS", 180, 180, nothing) # bounds for Upper...
cv.createTrackbar("U-S", "TrackBARS", 255, 255, nothing)
cv.createTrackbar("U-V", "TrackBARS", 255, 255, nothing)

cv.setTrackbarPos("L-H", "TrackBARS", 61)
cv.setTrackbarPos("L-S", "TrackBARS", 247)
cv.setTrackbarPos("L-V", "TrackBARS", 247)

while True:
    
    cv.imshow('Capture',frame)  # show the raw filtered image
    
    hsvFrame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    l_h = cv.getTrackbarPos("L-H", "TrackBARS")
    l_s = cv.getTrackbarPos("L-S", "TrackBARS")
    l_v = cv.getTrackbarPos("L-V", "TrackBARS")
    u_h = cv.getTrackbarPos("U-H", "TrackBARS")
    u_s = cv.getTrackbarPos("U-S", "TrackBARS")
    u_v = cv.getTrackbarPos("U-V", "TrackBARS")

    lowerHSV = np.array([l_h, l_s, l_v])
    upperHSV = np.array([u_h, u_s, u_v])

    mask = cv.inRange(hsvFrame,lowerHSV,upperHSV)  # apply the filtering mask with the HSV window
    cv.imshow('MASK_Frame',mask)

    key = cv.waitKey(10)

    if key == ord('q'):
        print("Closing app...")
        fobj.close()
        cv.destroyAllWindows()
        break



    