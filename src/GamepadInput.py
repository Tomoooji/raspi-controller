import pygame.joystick as joystick
import os
import json

class GamePad:
    def __init__(self, config_json, print_log = False):
        self.print_log = print_log
        #C:\Users\ka_po\Documents\Python_2026\raspi-controller\src\config\DualShock4.json
        with open(os.path.join(os.getcwd(),"raspi-controller","src","config", config_json), "r") as config:
            self.gamepad_info = json.load(config)
        self.gamepad = joystick.Joystick(0)
        self.states = {}#key:None for key in self.gamepad_info["Button"]}
        self.values = {}#key:None for key in self.gamepad_info["Axis"]}
    
    def onButtonDown(self, button):
        if self.print_log: print(self.gamepad.info["Button"][button])
        
        
    def onAxisMove(self, axis, value):
        if self.print_log: print(self.gamepad.info["Axis"][axis],value)
        
    
    def update(self):
        self.states = {button:self.gamepad.get_button(button) for button in self.gamepad_info["Button"]}
        self.values = {axis:self.gamepad.get_button(axis) for axis in self.gamepad_info["Axis"]}
        if self.print_log:
            print(self.states)
            print(self.values)

import pygame

def main():
    pygame.init()
    pad=GamePad("DualShock4.json",True)
    pygame.display.set_mode((300,300))
    while True:
        pad.update()
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                pad.onAxisMove(event.axis, event.value)
            if event.type == pygame.JOYBUTTONDOWN:
                pad.onButtonDown(event.button)
        pygame.display.update()
        
if __name__ == "__main__":
    main()