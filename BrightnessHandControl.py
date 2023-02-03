import cv2
import numpy as np
import time
import HandDetectionModule as hdm
import math

###############################
wCam, hCam = 640, 480
fingers = {
    "THUMB": 4,
    "INDEX": 8,
    "MIDDLE": 12,
    "RING": 16,
    "PINKY": 20
}
###############################

capture = cv2.VideoCapture(0)
capture.set(3, wCam) # Set Display width
capture.set(4, hCam) # Set Display height
pTime = 0
startTime = -1
detector = hdm.HandDetector(detectionCon=0.7)

open('test.txt', 'w').close()
currTime = time.time()
while True:
    success, img = capture.read()
    # Draws the hand
    detector.findHands(img, draw=False)
    lmlist = detector.findPosition(img, draw=False)
    if(len(lmlist) != 0):
        with open('test.txt', 'w') as f:
            # turn 5 finger's positions into string
            output_string = "{\n"
            for key in fingers:
                output_string += "\t{}:\tX:{} Y:{}\n".format(key, lmlist[fingers[key]][1], lmlist[fingers[key]][2])
            output_string += "}\n"

            f.write(output_string)
            print(output_string)

        x1, y1 = lmlist[fingers["THUMB"]][1], lmlist[fingers["THUMB"]][2]
        x2, y2 = lmlist[fingers["INDEX"]][1], lmlist[fingers["INDEX"]][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)

        # Draws a line between thumb and index and puts a dot on the center of the line
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 10)
        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        if(length < 30):
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
            if (startTime == -1):
                startTime = time.time()
                # print("This is wroking")
        elif(startTime != -1):
            endTime = time.time()
           # if (endTime - startTime >= 1) and (cx < 680 and cx > 480) and (cy < 200 and cy > 0):
                #if (sbc.get_brightness()[0] <= 10):
                    #sbc.set_brightness(100)
                #elif (sbc.get_brightness()[0] <= 100):
                    #sbc.set_brightness(0)
            #startTime = -1

        # inside length  < 30 have a bool that gets notted everytime that length < 30
        # if (true) then set brightness to whatever
        # either have bool control the enabling of set brightness or make the brightness a variable value that chnages
        # with each click so for now either 0 or 100

    cTime = time.time()
    fps = 1/ (cTime - pTime)
    pTime = cTime

    # FPS Display
    cv2.putText(img, f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 2)

    # Brightness Control
    #brightness = sbc.get_brightness()

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break