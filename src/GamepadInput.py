import pygame.joystick as joystick
import os
import json

class GamePad:
    def __init__(self, config_json, print_log = False):
        self.print_log = print_log
        with open(os.path.join(os.getcwd(),"raspi-controller","src","config", config_json), "r") as config:
            self.gamepad_info = json.load(config)
        self.is_connnect = False
        self.gamepad = None
        #self.states = {}
        #self.values = {}
        self.connect()
    
    def connect(self):
        for n in range(pygame.joystick.get_count()):
            self.gamepad = joystick.Joystick(n)
            if self.gamepad.get_name() == self.gamepad_info["Name"]:
                self.is_connnect = True
                print(f"connected:{self.gamepad.get_name()}")
                break
            else:
                print("unexpected controller may be connected")
                continue
        print("please connect controller to computer")
    
    def onButtonDown(self, button):
        if self.print_log: print(list(self.gamepad_info["Button"].keys())[button])
        #if self.gamepad_info["Button"][button] == "Button12":
            #print(self.values)
        
    def onAxisMove(self, axis, value):
        if self.print_log and abs(value)>0.3: print(list(self.gamepad_info["Axis"].keys())[axis],value)
        
    def onHatTilt(self, hat, value):
        if self.print_log: print(hat,value)
            
    def getInput(self):
        if "Button" in self.gamepad_info: self.gamepad_info["Button"] = {button:bool(self.gamepad.get_button(n)) for n,button in enumerate(self.gamepad_info["Button"])}
        if "Axis" in self.gamepad_info: self.gamepad_info["Axis"] = {axis:self.gamepad.get_axis(n) for n,axis in enumerate(self.gamepad_info["Axis"])}
        if "Hat" in self.gamepad_info: self.gamepad_info["Hat"] = {hat:{button:value for button,value in zip(self.gamepad_info["Hat"][hat].keys(),self.convertHat(self.gamepad.get_hat(n)))} for n,hat in enumerate(self.gamepad_info["Hat"].keys())}
        #values = [list(self.convertHat(self.gamepad.get_hat(n))) for n in range(self.gamepad.get_numhats())]
        #buttons = [list(self.gamepad_info["Hat"][hat].keys()) for hat in self.gamepad_info["Hat"]]
        #print(buttons[0])
        #print(values[0])
        #self.gamepad_info["Hat"] = {hat:dict(zip(buttons[n],values[n])) for n,hat in enumerate(self.gamepad_info["Hat"].keys())}
        
    def convertHat(self, value):
        return (value[0]>0, value[0]<0, value[1]>0, value[1]<0)
    
import pygame, sys

def main():
    pygame.init()
    pad=GamePad("DualShock4.json",True)#DualShock4#ElecomPad
    pygame.display.set_mode((300,300))
    while pad.is_connnect:
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
            if event.type == pygame.JOYDEVICEREMOVED:
                if pygame.joystick.get_count() == 0:
                    print("controller disconnected")
                    print("prgram will end...")
                    pad.is_connnect = False
                                
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        pad.getInput()
        pygame.display.update()
        
if __name__ == "__main__":
    main()