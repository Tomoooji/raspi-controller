import pygame, sys
from pygame.locals import *
from GamepadInput import GamePad
from GraphicalInterfase import GraphicInterfase as GUI

class Controller(GUI,GamePad):
    def __init__(self, config_widow, config_controller, print_log):
        GUI.__init__(self, config_widow, print_log)
        GamePad.__init__(self, config_controller, print_log)
        
    def convert(self):
        self.window_info["stick"][0]["value_x"] = self.values["LStickX"]
        self.window_info["stick"][0]["value_y"] = self.values["LStickY"]
        self.window_info["stick"][1]["value_x"] = self.values["RStickX"]
        self.window_info["stick"][1]["value_y"] = self.values["RStickY"]
        
    def main(self):
        pygame.init()
        GUI.begin(self)
        while GamePad.is_connecting:
            GamePad.getInput()
            self.convert()
            GUI.draw(self)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == JOYBUTTONDOWN:
                    GamePad.onButtonDown(self)
                if event.type == JOYAXISMOTION:
                    GamePad.onAxisMove(self)
                if event.type == JOYHATMOTION:
                    GamePad.onHatTilt(self)
            pygame.display.update()
                