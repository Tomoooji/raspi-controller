import pygame.joystick as joystick
import os.path as path
import json

class GamePad:
    def __init__(self, config_json, print_log = False):
        self.print_log = print_log
        with open(path.join("config", config_json), "r") as config:
            self.gamepad_info = json(config)
        self.gamepad = joystick.Joystick(0)
        self.states = {}#key:None for key in self.gamepad_info["Button"]}
        self.values = {}#key:None for key in self.gamepad_info["Axis"]}
    
    def onButtonDown(self, button):
        ...
        
    def onAxisMove(self, axis, value):
        ...
    
    def update(self):
        self.states = {button:self.gamepad.get_button(button) for button in self.gamepad_info["Button"]}
        self.values = {axis:self.gamepad.get_button(axis) for axis in self.gamepad_info["Axis"]}
        if self.print_log:
            print(self.states)
            print(self.values)
    