import numpy as np
import cv2
from matplotlib import pyplot as plt
import time

import socket
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 22222
Message = "0"
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#lower = { 'blue':(100,100,100),'green':(40, 40, 100),'orange':(5, 40, 100),'red':(166, 84, 141) }
#upper = { 'blue':(140,255,255),'green':(60,255,255),'orange':(20,255,255),'red':(186,255,255)}

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (50,50)
fontScale              = 1
color              = (0,255,0)
thickness              = 2

img_width, img_height = 400,300
dim = (img_width, img_height)

lower_blue = np.array([100,100,60])
upper_blue = np.array([150,255,200])

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    #frame = cv2.convertScaleAbs(frame, alpha=1, beta=-20)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    blur = cv2.blur(hsv,(3,3))
    #blur = cv2.GaussianBlur(hsv,(2,2),3)
    #median = cv2.medianBlur(hsv,5)
    hsv=blur

    kernel = np.ones((5,5),np.uint8)
    #closing = cv2.morphologyEx(hsv, cv2.MORPH_CLOSE, kernel)
    #hsv=closing


    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow('mask',mask)
    

    contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]

    areas = [cv2.contourArea(c) for c in contours]
    #print(areas)
    try:
        max_index = np.argmax(areas)
        cnt=contours[max_index]
        M = cv2.moments(cnt)
        #print(M)
        
        area = cv2.contourArea(cnt)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print(area)
        print(cx,cy)
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(hsv,(x,y),(x+w,y+h),(0,255,0),2)

        Message=str(-(cx-320)*(3.7/320))

        clientSock.sendto(bytes(Message,'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
    except:
        clientSock.sendto(bytes(Message,'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
    #print("none exist")
        pass

    frame = cv2.putText(hsv, str(str(cx)+","+str(Message)), (cx,cy), font,  fontScale, color, thickness, cv2.LINE_AA) 
    cv2.imshow("frame",frame)

    cv2.waitKey(1)