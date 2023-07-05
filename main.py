import PySimpleGUI as sg
from client import HandTrackClient
from multiprocessing import Process
import threading

class MenuScreen:

    def __init__(self):
        sg.change_look_and_feel('Default1')
        layout = [
            [sg.Text('Host:', justification='l'), sg.InputText('169.254.96.88',size=(15,0), key='host')],
            [sg.Text('Porta:'), sg.Spin([i for i in range(10000,55600)],initial_value=55555, key='porta', size=(5,0), auto_size_text=False)],
            [sg.Text('Sensibilidade do cursor:'), sg.Spin([i for i in range(1,10)],initial_value=4, key='sensibilidade', size=(2,0))],
            [sg.Button('Start', key='_START_'), sg.Button('Stop',disabled=True, key='_STOP_')],
        ]

        self.janela = sg.Window("Hand Track", size=(300,200), element_padding=10).layout(layout)

    def initScreen(self, htc: HandTrackClient):
        while True:
            self.event, self.values = self.janela.read()
            if self.event == sg.WIN_CLOSED:
                htc.run = False
                break
            elif self.event == '_START_':
                self.janela['_START_'].update(disabled=True)
                self.janela['_STOP_'].update(disabled=False)
                htc.host = self.values['host']
                htc.port = int(self.values['porta'])
                htc.setMouseSens(int(self.values['sensibilidade']))
                htc.run = True
                threading.Thread(target=htc.runClient).start()
            elif self.event == '_STOP_':
                self.janela['_START_'].update(disabled=False)
                self.janela['_STOP_'].update(disabled=True)
                htc.run = False


screen = MenuScreen()
htc = HandTrackClient()
screen.initScreen(htc)
