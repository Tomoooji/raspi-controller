import sys
import pygame
from pygame.locals import *
import serial

window_config = {
    "size":(800,600),
    "fps":60,
    "title":"RasPi Controller"
    }
serial_config = {"port":"COM5", "boundrate":115200}
dualshock_config = {"keys":[]}

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
            
            if self.window_info: pygame.display.update()
    
    def setup(self):
        pygame.init()
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
        pygame.display.set_mode(self.window_info.get("size",(800,600)))
        if "title" in self.window_info: pygame.display.set_caption(self.window_info["title"])
    
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