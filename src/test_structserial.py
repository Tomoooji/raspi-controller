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
        screen = pygame.display.set_mode((500,500))
        pygame.time.wait(2000)
        tick = pygame.time.Clock()
        while self.is_connnect and self.serial.is_open:
            GP.getInput(self)

            self.serial_info["send_data"]["dist"] = 255 *np.hypot(
                self.gamepad_info["Axis"]["LStickX"],
                self.gamepad_info["Axis"]["LStickY"]
            ).clip(0,1)
            
            self.serial_info["send_data"]["angle"] = np.degrees(np.arctan2(
                self.gamepad_info["Axis"]["LStickY"],
                self.gamepad_info["Axis"]["LStickX"]
            ))%360 if self.serial_info["send_data"]["dist"]>0.1 else 0
            
            self.serial_info["send_data"]["turn"] = 255 *(
                (self.gamepad_info["Axis"]["R2"]+1) - (self.gamepad_info["Axis"]["L2"]+1)
            )
            
            if self.print_log: print("send",self.serial_info["send_data"])
            SC.send_dict(self)
            SC.receive_dict(self)
            if self.print_log: print("receive",self.serial_info["receive_data"])
            ##print(self.serial.readline().decode('utf-8').strip())

            screen.fill((0,0,0))
            pygame.draw.rect(screen,(100,0,0),(10,10,abs(self.serial_info["send_data"]["angle"]),20))
            pygame.draw.rect(screen,(100,0,0),(10,30,self.serial_info["send_data"]["dist"],20))
            pygame.draw.rect(screen,(100,0,0),(10,50,abs(self.serial_info["send_data"]["turn"]),20))
            
            pygame.draw.rect(screen,(0,100,0),(10,70,abs(self.serial_info["receive_data"]["angle"]),20))
            pygame.draw.rect(screen,(0,100,0),(10,90,self.serial_info["receive_data"]["dist"],20))
            pygame.draw.rect(screen,(0,100,0),(10,110,abs(self.serial_info["receive_data"]["turn"]),20))
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == JOYBUTTONDOWN:
                    GP.onButtonDown(self,event.button)
                if event.type == JOYAXISMOTION:
                    GP.onAxisMove(self,event.axis,event.value)
                if event.type == JOYHATMOTION:
                    GP.onHatTilt(self,event.hat,event.value)
                
            tick.tick(100)
            pygame.display.update()
            
if __name__ == "__main__":
    test = Controller("ESP32.json","DualShock4.json",False)
    test.main()