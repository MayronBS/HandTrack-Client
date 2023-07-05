from pynput.keyboard import Key, Controller as keycontroller
from pynput.mouse import Button, Controller
import autopy
import numpy as np
import math

class HandCommand:
    def __init__(self):
        self.oldCoordX = 0
        self.oldCoordY = 0
        self.mouseCoordX = 0
        self.mouseCoordY = 0
        self.key = keycontroller()
        self.mouse = Controller()
        self.buttonPressed = False

    def executeCommand(self, coordList: list, screenWidth):
        extendedFingers = self.extendedFingers(coordList)
        actDistance = self.actDistance(self.handDistance(coordList))
        fingerDistance = self.fingersDistance(coordList,4,5)
        activate = fingerDistance < actDistance

        if extendedFingers == [1, 0, 0, 0]:
            self.leftMouseButton(activate)
            self.mouseMove(screenWidth)
        elif extendedFingers == [1, 1, 0, 0]:
            self.rightMouseButton(activate)
            self.mouseMove(screenWidth)
        elif extendedFingers == [1, 0, 0, 1]:
            self.midleMouseButton(activate)
            self.mouseMove(screenWidth)
        elif (extendedFingers.count(1) >= 3) and (self.fingersDistance(coordList,4,8) < actDistance):
            self.mouseScroll()
        elif (extendedFingers.count(1) >= 3) and (self.fingersDistance(coordList,4,12) < actDistance):
            self.volumeControll()
        else:
            self.mouseMove(screenWidth)
            self.buttonsDepress()


    #Funcionalidades

    def leftMouseButton(self, activate: bool):
        if activate:
            if self.buttonPressed == False:
                self.mouse.press(Button.left)
                self.buttonPressed = True
        elif self.buttonPressed == True:
                self.mouse.release(Button.left)
                self.buttonPressed = False

    def rightMouseButton(self, activate: bool):
        if activate:
            if self.buttonPressed == False:
                self.mouse.press(Button.right)
                self.buttonPressed = True
        elif self.buttonPressed == True:
                self.mouse.release(Button.right)
                self.buttonPressed = False

    def midleMouseButton(self, activate: bool):
        if activate:
            if self.buttonPressed == False:
                self.mouse.press(Button.middle)
                self.buttonPressed = True
        elif self.buttonPressed == True:
                self.mouse.release(Button.middle)
                self.buttonPressed = False

    def mouseScroll(self):
        scrollY =  (self.oldCoordY - self.mouseCoordY) / 15
        self.mouse.scroll(0, scrollY)

    def volumeControll(self):
        if (self.oldCoordY - self.mouseCoordY) < 0:
            self.key.tap(Key.media_volume_down)
        else:
            self.key.tap(Key.media_volume_up)

    def mouseMove(self, screenWidth):
        try:
            autopy.mouse.move(screenWidth - self.mouseCoordX, self.mouseCoordY)
        except ValueError:
            print(ValueError)


    #Sets

    def setMouseCoords(self, coordX, coordY, mouseSens):
        self.mouseCoordX = self.oldCoordX + (coordX - self.oldCoordX) / mouseSens
        self.mouseCoordY = self.oldCoordY + (coordY - self.oldCoordY) / mouseSens

    def setOldCoords(self):
        self.oldCoordX = self.mouseCoordX
        self.oldCoordY = self.mouseCoordY

    #######

    def buttonsDepress(self):
        if self.buttonPressed:
            self.mouse.release(Button.left)
            self.mouse.release(Button.right)
            self.mouse.release(Button.middle)
            self.buttonPressed = False

    def extendedFingers(self, coordList: list):
        pontaDedos = [4, 8, 12, 16, 20]
        extendedFingers = []
        for id in range(1, 5):
            if coordList[pontaDedos[id]][2] < coordList[pontaDedos[id] - 2][2]:
                extendedFingers.append(1)
            else:
                extendedFingers.append(0)
        return extendedFingers

    def handDistance(self, coordList: list):
        x1, x2 = coordList[2][1], coordList[1][1]
        y1, y2 = coordList[2][2], coordList[1][2]
        handDistance = math.hypot(x2 - x1, y2 - y1)
        return handDistance

    def fingersDistance(self, coordList: list, p1: int, p2: int):
        x1, x2 = coordList[p1][1], coordList[p2][1]
        y1, y2 = coordList[p1][2], coordList[p2][2]
        fingersDistance = math.hypot(x2 - x1, y2 - y1)
        return fingersDistance

    def actDistance(self, handDistance: int):
        actDistance = np.interp(handDistance, (10, 70), (15, 74))
        return actDistance
