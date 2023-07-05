import socket
import json
import autopy
import numpy as np
import math
from pynput.mouse import Button, Controller
from HandCommand import HandCommand
import PySimpleGUI as sg


class HandTrackClient:
    def __init__(self):
        self.screenWidth, self.screenHeight = autopy.screen.size()
        self.camWidth, self.camHeight = 640, 480
        self.marginSide, self.marginTop, self.marginDown = 110, 50, 150
        self.mouseSens: int = 3
        self.host: str = '169.254.96.88'
        self.port: int = 55555
        self.run: bool = True

    def runClient(self):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sk.connect((self.host, self.port))
        except:
            sg.popup_no_buttons('Não foi possível se conectar!')
            return
        handCommand = HandCommand()
        while self.run:

            try:
                dados = sk.recv(1024)
                coordList = json.loads(dados.decode())
            except:
                break

            if len(coordList) != 0:
                coordX = np.interp(coordList[8][1], (self.marginSide, self.camWidth - self.marginSide),
                                   (0, self.screenWidth))
                coordY = np.interp(coordList[8][2], (self.marginTop, self.camHeight - self.marginDown),
                                   (0, self.screenHeight))

                handCommand.setMouseCoords(coordX, coordY, self.mouseSens)

                handCommand.executeCommand(coordList, self.screenWidth)

                handCommand.setOldCoords()
        sk.close()

    def setMouseSens(self, value: int):
        if value > 0:
            self.mouseSens = value
