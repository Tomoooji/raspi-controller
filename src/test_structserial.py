"""
test program for checking SerialCommunication.py with GamepadInput.py
correct input data from DualShock4 and send to ESP32, get echo from it
if it pass the consol test, I'd like to control mecanum(or 4 omuni) wheels
result:
    not yet
"""
import numpy as np
import pygame,sys
from pygame.locals import *
from SerialCommunication import SerialCommunicater as SC
from GamepadInput import GamePad as GP

class Controller(SC,GP):
    def __init__(self,config_serial,config_gamepad,print_log):
        pygame.init()
        SC.__init__(self,config_serial,print_log)
        GP.__init__(self,config_gamepad,print_log)
    
    def main(self):
        SC.begin(self)
        pygame.display.set_mode((200,200))
        pygame.time.wait(2000)
        while self.is_connnect and self.serial.is_open:
            """
            self.serial_info["send_data"]["angle"] = np.degrees(np.arctan2(
                self.gamepad_info["Axis"]["LStickY"],
                self.gamepad_info["Axis"]["LStickX"]
            ))%360
            
            self.serial_info["send_data"]["dist"] = 255 *np.hypot(
                self.gamepad_info["Axis"]["LStickX"],
                self.gamepad_info["Axis"]["LStickY"]
            ).clip(0,1)
            
            self.serial_info["send_data"]["turn"] = 255 *(
                (self.gamepad_info["Axis"]["R2"]+1) - (self.gamepad_info["Axis"]["L2"]+1)
            )
            """
            SC.send_dict(self)
            SC.receive_dict_(self)
            #print(self.serial_info["receive_data"])
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == JOYBUTTONDOWN:
                    GP.onButtonDown(self,event.button)
                if event.type == JOYAXISMOTION:
                    GP.onAxisMove(self,event.type,event.value)
                if event.type == JOYHATMOTION:
                    GP.onHatTilt(self,event.hat,event.value)
                
            pygame.display.update()
            
if __name__ == "__main__":
    test = Controller("ESP32.json","DualShock4.json",True)
    test.main()