import pygame.joystick as joystick
import os
import json

class GamePad:
    def __init__(self, config_json, print_log = False):
        self.print_log = print_log
        with open(os.path.join(os.getcwd(),"raspi-controller","src","config", config_json), "r") as config:
            self.gamepad_info = json.load(config)
        self.gamepad = joystick.Joystick(0)
        self.states = {}
        self.values = {}
    
    def onButtonDown(self, button):
        if self.print_log: print(self.gamepad_info["Button"][button])
        #if self.gamepad_info["Button"][button] == "Button12":
            #print(self.values)
        
    def onAxisMove(self, axis, value):
        if self.print_log: print(self.gamepad_info["Axis"][axis],value)
        
    def onHatTilt(self, hat, value):
        if self.print_log: print(hat,value)
    
    def update(self):
        self.states = {button:self.gamepad.get_button(n) for n,button in enumerate(self.gamepad_info["Button"])}
        for n,hat in enumerate(self.gamepad_info.get("Hat",[])):
            value = self.gamepad.get_hat(n)
            self.states[hat[0]] = value[1] == 1
            self.states[hat[1]] = value[1] ==-1
            self.states[hat[2]] = value[0] == 1
            self.states[hat[3]] = value[0] ==-1
        self.states
        self.values = {axis:self.gamepad.get_axis(n) for n,axis in enumerate(self.gamepad_info["Axis"])}
        if self.print_log:
            #print(self.states)
            #print(self.values)
            pass

import pygame, sys

def main():
    pygame.init()
    pad=GamePad("ElecomPad.json",True)#DualShock4
    pygame.display.set_mode((300,300))
    while True:
        pad.update()
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                #print(event.axis, event.value)
                pad.onAxisMove(event.axis, event.value)
            if event.type == pygame.JOYBUTTONDOWN:
                #print(event.button)
                pad.onButtonDown(event.button)
            if event.type == pygame.JOYHATMOTION:
                if event.value[0]+event.value[1]:
                    pad.onHatTilt(event.hat, event.value)
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        pygame.display.update()
        
if __name__ == "__main__":
    main()