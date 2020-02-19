import cv2

def show_webcam(mirror=False):
    while True:
        pic = cv2.imread('kayaker2.jpg')
        pic_2 = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        hsv_pic = cv2.cvtColor(pic_2, cv2.COLOR_RGB2HSV)
        cv2.imshow('Main', pic)
        cv2.imshow('RGB', pic_2)
        cv2.imshow('HSV', hsv_pic)
        if cv2.waitKey(1) == 27:
            break
    
    cv2.destroyAllWindows()

show_webcam(mirror=True)

