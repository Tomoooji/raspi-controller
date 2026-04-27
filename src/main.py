import sys
import pygame
from pygame.locals import *
import serial

window_config = {"size":(800,600), "fps":60}
serial_config = {"port":"COM5", "boundrate":115200}
dualshock_config = {}

class Controller:
    def __init__(self, window_info={}, serial_info={}, controller_info={}):
        self.window_info = window_info
        self.serial_info = serial_info
        self.controller_info = controller_info

    def main(self):
        self.setup()
        while True:
            self.loop()
            for event in pygame.event.get():
                if self.controller_info and event.type in self.controller_info.get("keys"):
                    self.getinput()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
    
    def setup(self):
        if self.window_info:
            self.setWindow()
        if self.serial_info:
            self.beginSerial()
        
    def loop(self):
        if self.window_info:
           self.updateWindow()
        if self.serial_info:
            self.sendSerial() 
    

    def setWindow(self):
        ...
    
    def updateWindow(self):
        ...
        

    def beginSerial(self):
        ...
    
    def sendSerial(self):
        ...
        

    def watchValue(self):
        ...

    def getEvent(self):
        ...

if __name__ == "__main__":
    obj = Controller(
        window_info = window_config,
        serial_info = serial_config,
        controller_info = dualshock_config
    )
    obj.main()