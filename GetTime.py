import cv2
import numpy as np
import math



def getTimeFromClock(image):
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    center = None
    Hour, Minute, Second = 0, 0, 0

    h, w, c = img.shape
    if(w < 450):
        img = cv2.resize(img, (520, 520))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    #Draw one circle bouding face clock
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 250)
    for i in circles[0,:]:
        i[2]=i[2]+4
        cv2.circle(img,(int(i[0]),int(i[1])),int(i[2]),(0,255,0),2)
        cv2.circle(img,(int(i[0]),int(i[1])),2,(0,0,255),3)
        center = (int(i[0]),int(i[1]))

    # Apply edge detection (can use Canny edge detection)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Apply Hough Line Transform to detect line segments
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

    # Draw only one line for hour hand and one line for minute hand
    if lines is not None:
        countHour, countMinute, countSecond = 0, 0, 0
        for line in lines:
            Flag = False
            x1, y1, x2, y2 = line[0]
            length = math.sqrt((x2-x1)**2+(y2-y1)**2)

            if(210 > length > 195 and countSecond == 0):
                len = math.sqrt((center[0]-x1)**2+(center[0]-y1)**2)
                if(len > 100):
                    cv2.line(img, (center[0], center[1]), (x1, y1), (0,255,0), 2)
                    cv2.rectangle(img, (center[0], center[1]), (x1, y1), (0,255,0), 2)
                    cv2.putText(img, "Second", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                else:
                    cv2.line(img, (center[0], center[1]), (x2, y2), (0,255,0), 2)
                    cv2.rectangle(img, (center[0], center[1]), (x2, y2), (0,255,0), 2)
                    cv2.putText(img, "Second", (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    Flag = True

                countSecond = 1
                #Get angle between two vector
                vector1 = np.array([center[0]-center[0], center[1]-(-200)])
                vector2 = np.array([x1-x2, y1-y2])
                cos = np.dot(vector1, vector2)/(np.linalg.norm(vector1)*np.linalg.norm(vector2))
                angle = np.arccos(cos)
                angle = angle*180/np.pi
                if(Flag == True):
                    if(x2 < center[0] and angle != 0):
                        angle = 180 + angle
                else:
                    if(x1 < center[0] and angle != 0):
                        angle = 180 + angle
                Second = angle

            if(140 < length < 155 and countHour == 0):
                len = math.sqrt((center[0]-x1)**2+(center[0]-y1)**2)
                if(len > 100):
                    cv2.line(img, (center[0], center[1]), (x1, y1), (0, 0, 255), 2)
                    cv2.rectangle(img, (center[0], center[1]), (x1, y1), (0,0,255), 2)
                    cv2.putText(img, "Hour", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.line(img, (center[0], center[1]), (x2, y2), (0, 0, 255), 2)
                    cv2.rectangle(img, (center[0], center[1]), (x2, y2), (0,0,255), 2)
                    cv2.putText(img, "Hour", (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    Flag = True

                countHour = 1

                #Get angle between two vector
                vector1 = np.array([center[0]-center[0], center[1]-(-200)])
                vector2 = np.array([x1-x2, y1-y2])
                cos = np.dot(vector1, vector2)/(np.linalg.norm(vector1)*np.linalg.norm(vector2))
                angle = np.arccos(cos)
                angle = angle*180/np.pi
                if(Flag == True):
                    if(x2 < center[0] and angle != 0):
                        angle = 180 + angle
                else:
                    if(x1 < center[0] and angle != 0):
                        angle = 180 + angle
                Hour = angle
            
            if(155 < length < 195 and countMinute == 0):
                len = math.sqrt((center[0]-x1)**2+(center[0]-y1)**2)
                if(len > 100):
                    cv2.line(img, (center[0], center[1]), (x1, y1), (255, 0, 0), 2)
                    cv2.rectangle(img, (center[0], center[1]), (x1, y1), (255,0,0), 2)
                    cv2.putText(img, "Minute", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                else:
                    cv2.line(img, (center[0], center[1]), (x2, y2), (255, 0, 0), 2)
                    cv2.rectangle(img, (center[0], center[1]), (x2, y2), (255,0,0), 2)
                    cv2.putText(img, "Minute", (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                    Flag = True

                countMinute = 1

                #Get angle between two vector
                vector1 = np.array([center[0]-center[0], center[1]-(-200)])
                vector2 = np.array([x1-x2, y1-y2])
                cos = np.dot(vector1, vector2)/(np.linalg.norm(vector1)*np.linalg.norm(vector2))
                angle = np.arccos(cos)
                angle = angle*180/np.pi
                if(Flag == True):
                    if(x2 < center[0] and angle != 0):
                        angle = 180 + angle
                else:
                    if(x1 < center[0] and angle != 0):
                        angle = 180 + angle
                Minute = angle


    #Get time from angle
    Minute = int(Minute/6)
    Second = int(Second/6)

    if(Minute < 40):
        Hour = Hour/30
        temp = int(Hour)
        if(Hour > (int(Hour))+ 0.9):
            Hour = int(Hour) + 1
        else:
            Hour = temp
    else:
        Hour = int(Hour/30)

    Time = ""
    if(Hour < 10):
        if(Hour == 0):
            Hour = 12
            Time = str(Hour) + ":"
        else:
            Time = "0" + str(Hour) + ":"
    else:
        Time = str(Hour) + ":"

    if(Minute < 10):
        Time = Time + "0" + str(Minute) + ":"
    else:
        Time = Time + str(Minute) + ":"

    if(Second < 10):
        Time = Time + "0" + str(Second)
    else:
        Time = Time + str(Second)

    cv2.putText(img, Time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imwrite("Result_" + image, img)
    

for i in range(0, 5):
    path = "Clock" + str(i) + ".png"
    getTimeFromClock(path)