import pygame,sys
from pygame.locals import *

def main():
    pygame.init()
    if not pygame.joystick.get_count():
        print("no controller connected")
        return
    ctr=pygame.joystick.Joystick(0)
    print(f"name:{ctr.get_name()}")
    print(f"button:{ctr.get_numbuttons()}")
    print(f"axis:{ctr.get_numaxes()}")
    print(f"hat:{ctr.get_numhats()}")
    connecting=True
    pygame.display.set_mode((200,200))
    while connecting:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==JOYAXISMOTION:
                if event.value>0.5:
                    print(f"Axis:{event.axis} {event.value}")
            if event.type==JOYBUTTONDOWN:
                print(f"Button:{event.button}")
            if event.type==JOYHATMOTION:
                print(f"Hat:{event.hat}")
            if event.type==JOYDEVICEREMOVED:
                connecting=False
        pygame.display.update()
        
if __name__ == "__main__":
    main()