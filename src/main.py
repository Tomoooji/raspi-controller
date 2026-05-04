import pygame,sys
from pygame.locals import *

from GamepadInput import GamePad as GP
from GraphicalInterface import GraphicInterface as GI
from SerialCommunication import SerialCommunicater as SC


class Controller(GP,GI,SC):
    def __init__(self, config_gamepad, config_window, config_serial, print_log):
        pygame.init()
        GP.__init__(self,config_gamepad, print_log)
        GI.__init__(self,config_window)
        SC.__init__(self,config_serial, print_log)
        self.is_running = False
        self.clock = pygame.time.Clock()
        self.fps = 60
        
    def updateSerialInput(self):
        ...
    
    def updateWindowInfo(self):
        # window_info側にtagを付けてるのでもっと賢く書くことも当然できるが、ぶっちゃけ2,3個動けば問題ないのでそこはご愛嬌
        self.window_info["rect"][0]["activated"] = self.gamepad_info["Button"]["Touchpad"]
        
        self.window_info["circle"][0]["activated"] = self.gamepad_info["Button"]["Square"]
        self.window_info["circle"][1]["activated"] = self.gamepad_info["Button"]["Circle"]
        self.window_info["circle"][2]["activated"] = self.gamepad_info["Button"]["Triangle"]
        self.window_info["circle"][3]["activated"] = self.gamepad_info["Button"]["Cross"]
        
        self.window_info["circle"][4]["activated"] = self.gamepad_info["Button"]["Right"]
        self.window_info["circle"][5]["activated"] = self.gamepad_info["Button"]["Left"]
        self.window_info["circle"][6]["activated"] = self.gamepad_info["Button"]["Up"]
        self.window_info["circle"][7]["activated"] = self.gamepad_info["Button"]["Down"]
        
        self.window_info["circle"][8]["activated"] = self.gamepad_info["Button"]["Option"]
        self.window_info["circle"][9]["activated"] = self.gamepad_info["Button"]["Share"]
        self.window_info["circle"][10]["activated"] = self.gamepad_info["Button"]["PSButton"]

        self.window_info["bar_h"][0]["value"] = self.gamepad_info["Axis"]["R2"]
        self.window_info["bar_h"][1]["value"] = self.gamepad_info["Axis"]["L2"]
        
        self.window_info["bar_h"][2]["activated"] = self.gamepad_info["Button"]["R1"]
        self.window_info["bar_h"][3]["activated"] = self.gamepad_info["Button"]["L1"]

        self.window_info["stick"][0]["value_x"] = self.gamepad_info["Axis"]["RStickX"]
        self.window_info["stick"][0]["value_y"] = -self.gamepad_info["Axis"]["RStickY"]
        self.window_info["stick"][0]["activated"] = -self.gamepad_info["Button"]["R3"]

        self.window_info["stick"][1]["value_x"] = self.gamepad_info["Axis"]["LStickX"]
        self.window_info["stick"][1]["value_y"] = -self.gamepad_info["Axis"]["LStickY"]
        self.window_info["stick"][1]["activated"] = -self.gamepad_info["Button"]["L3"]
        
    def createSerialMessage(self):
        ...
        
    def setup(self):
        SC.begin(self)
        GI.begin(self)        
        
    def loop(self):
        SC.receive(self)
        self.updateSerialInput()
        GP.getInput(self)
        self.createSerialMessage()
        SC.send(self)
        self.updateWindowInfo()
        GI.draw(self)
        
        pygame.display.update()
        self.clock.tick(self.fps)

        
    def main(self):
        self.setup()
        while self.is_runnig:
            self.loop()
            for event in pygame.event.get():
                if event.type == QUIT:
                    ...
            
    
if __name__ == "__main__":
    obj = Controller(
        "DualShock4.json",
        "DS4Window.json",
        "ESP32.json"
    )
    obj.main()