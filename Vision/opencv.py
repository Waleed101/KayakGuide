import cv2
import numpy as np


def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        _, frame = cam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([30,150,50])
        upper_red = np.array([255,255,180])
        
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(frame,frame, mask= mask)

        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        cv2.imshow('res',res)
        # ret_val, img = cam.read()
        # if mirror: 
        #     img = cv2.flip(img, 1)
        # cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()