
import mediapipe
import cv2
import time
import json
import autopy
import numpy as np
import math
from pynput.mouse import Button, Controller
from HandCommand import HandCommand

#teste do processo de rastreio no PC

drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands
camWidth, camHeight = 640, 480

screenWidth, screenHeight = autopy.screen.size()
marginSide, marginTop, marginDown = 90, 25, 125

mouseSens = 4
distanceBase = 90
oldCoordX, oldCoordY = 0, 0
mouseCoordX, mouseCoordY = 0, 0
mouse = Controller()
mouseButtonPressed = False

hc = HandCommand()


cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

pframe = 0

with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.1,
                       max_num_hands=1) as hands:
    while True:
        ret, frame = cap.read()
        frame1 = cv2.resize(frame, (camWidth, camHeight))

        # FPS
        cframe = time.time()
        fps = 1 / (cframe - pframe)
        pframe = cframe
        # print(fps)
        #cv2.putText(frame1, f'{int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX, 1,(255,0,0), 2)

        #cv2.rectangle(frame1, (marginSide, marginTop), (camWidth - marginSide, camHeight - marginDown), (255, 0, 0), 1)

        results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))

        coordList = []
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)

                for point in handsModule.HandLandmark:
                    normalizedLandmark = handLandmarks.landmark[point]
                    coordX, coordY = int(normalizedLandmark.x * camWidth), int(normalizedLandmark.y * camHeight)
                    coordList.append([int(point), coordX, coordY])

        stringlist = str(coordList)
        print(stringlist)
        coordList = json.loads(stringlist)

        if len(coordList) != 0:
            coordX = np.interp(coordList[8][1], (marginSide, camWidth - marginSide), (0, screenWidth))
            coordY = np.interp(coordList[8][2], (marginTop, camHeight - marginDown), (0, screenHeight))

            hc.setMouseCoords(coordX, coordY, mouseSens)

            hc.executeCommand(coordList, screenWidth)

            hc.setOldCoords()


        cv2.imshow("HandTrack Test", frame1)
        key = cv2.waitKey(1) & 0xFF

        # if the |q| is press on the keyboard it will stop the system
        if key == ord("q"):
            break
