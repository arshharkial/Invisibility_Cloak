import cv2
import numpy as np
import time

video = cv2.VideoCapture(0)
time.sleep(3)

for i in range(60):
    check, background = video.read()
background = np.flip(background, axis = 1)

while(video.isOpened):
    check, image = video.read()
    if not check:
        break
    
    image = np.flip(image, axis = 1)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 120, 50])
    upper = np.array([10, 255, 255])
    filter1 = cv2.inRange(hsv, lower, upper)
    lower = np.array([170, 120, 70])
    upper = np.array([180, 255, 255])
    filter2 = cv2.inRange(hsv, lower, upper)
    filter1 = filter1 + filter2
    filter1 = cv2.morphologyEx(filter1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    filter1 = cv2.morphologyEx(filter1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    filter2 = cv2.bitwise_not(filter1)
    result1 = cv2.bitwise_and(image, image, mask = filter2)
    result2 = cv2.bitwise_and(background, background, mask = filter1)
    final = cv2.addWeighted(result1, 1, result2, 1, 0)
    cv2.imshow("Final", final)
    key = cv2.waitKey(10) 
    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows()