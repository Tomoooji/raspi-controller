import pygame, sys
from pygame.locals import *
from GamepadInput import GamePad
from GraphicalInterface import GraphicInterface as GUI

class Controller(GUI,GamePad):
    def __init__(self, config_widow, config_controller, print_log):
        pygame.init()
        GUI.__init__(self, config_widow)
        GamePad.__init__(self, config_controller, print_log)
        
    def convert(self):
        self.window_info["rect"][0]["activated"] = self.gamepad_info["Button"]["Touchpad"]
        
        self.window_info["circle"][0]["activated"] = self.gamepad_info["Button"]["Square"]
        self.window_info["circle"][1]["activated"] = self.gamepad_info["Button"]["Circle"]
        self.window_info["circle"][2]["activated"] = self.gamepad_info["Button"]["Triangle"]
        self.window_info["circle"][3]["activated"] = self.gamepad_info["Button"]["Cross"]
        
        self.window_info["circle"][4]["activated"] = self.gamepad_info["Button"]["Right"]
        self.window_info["circle"][5]["activated"] = self.gamepad_info["Button"]["Left"]
        self.window_info["circle"][6]["activated"] = self.gamepad_info["Button"]["Up"]
        self.window_info["circle"][7]["activated"] = self.gamepad_info["Button"]["Down"]

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
        
    def main(self):
        GUI.begin(self)
        while self.is_connnect:#GamePad.connecting:
            GamePad.getInput(self)
            self.convert()
            GUI.draw(self)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == JOYBUTTONDOWN:
                    GamePad.onButtonDown(self,event.button)
                if event.type == JOYAXISMOTION:
                    GamePad.onAxisMove(self,event.type,event.value)
                if event.type == JOYHATMOTION:
                    GamePad.onHatTilt(self,event.hat,event.value)
            pygame.display.update()

if __name__ == "__main__":
    test = Controller("laptop.json","DualShock4.json",False)
    test.main()