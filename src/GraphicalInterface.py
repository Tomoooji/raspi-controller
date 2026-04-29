import pygame
import json
import os

class GraphicInterface:
    def __init__(self,config_json):
        with open(os.path.join(os.getcwd(),"raspi-controller","src","config",config_json), "r") as config:
            self.window_info = json.load(config)
        self.screen = None
        
    
    def begin(self):
        self.screen = pygame.display.set_mode(self.window_info["size"])
        if "title" in self.window_info:
            pygame.display.set_caption(self.window_info["title"])
    
    def draw(self):
        self.screen.fill(self.window_info["color"]["background"])
        if "rect" in self.window_info:
            for args in self.window_info["rect"]:
                rect = pygame.Rect(0,0,args["width"],args["height"])
                rect.center = (self.window_info["origin"][0]+args["center_x"], self.window_info["origin"][1]-args["center_y"])
                pygame.draw.rect(
                    self.screen,
                    self.window_info["color"]["active" if args["activated"] else "base"],
                    rect,
                    5
                )
        
        if "circle" in self.window_info:
            for args in self.window_info["circle"]:
                pygame.draw.circle(
                    self.screen,
                    self.window_info["color"]["active" if args["activated"] else "base"],
                    (self.window_info["origin"][0]+args["center_x"], self.window_info["origin"][1]-args["center_y"]),
                    args["radius"]
                )
        
        if "stick" in self.window_info:
            for args in self.window_info["stick"]:
                pygame.draw.circle(
                    self.screen,
                    self.window_info["color"]["base"],
                    (self.window_info["origin"][0]+args["center_x"],self.window_info["origin"][1]-args["center_y"]),
                    args["out_radius"],
                    5
                )
                pygame.draw.circle(
                    self.screen,
                    self.window_info["color"]["active" if args.get("activated",False) else "base"],
                    (self.window_info["origin"][0]+args["value_x"]*args["out_radius"]+args["center_x"], self.window_info["origin"][1]-(args["value_y"]*args["out_radius"]+args["center_y"])),
                    args["in_radius"]
                )

        if "bar_h" in self.window_info:
            for args in self.window_info["bar_h"]:
                pygame.draw.line(
                    self.screen,
                    self.window_info["color"]["active" if "activated" in args and args["activated"] else "base"],
                    (self.window_info["origin"][0]+args["center_x"]-(args["width"]/2),self.window_info["origin"][1]-args["center_y"]),
                    (self.window_info["origin"][0]+args["center_x"]+(args["width"]/2),self.window_info["origin"][1]-args["center_y"]),
                    args["height"]
                )
                if "value" in args:
                    pygame.draw.line(
                        self.screen,
                        self.window_info["color"]["active"],
                        (self.window_info["origin"][0]+args["center_x"]-(args["width"]/2)-1, self.window_info["origin"][1]-args["center_y"]),
                        (self.window_info["origin"][1]+args["center_x"]-(args["width"]/4)+(args["value"]*args["width"]/2), self.window_info["origin"][1]-args["center_y"]),
                        args["height"]
                    )
                # lineだと端が四角だがaalineは太さを指定できない
                # 両端は〇の方が良いかもしれない
                #pygame.draw.circle(
                #    self.screen,
                #    self.window_info["color"][1],
                #    ((args["width"]-args["height"])/2 + args["center_x"], args["center_y"]),
                #    args["width"]/2
                #)
                #pygame.draw.circle(
                #    self.screen,
                #    self.window_info["color"][1],
                #    ((args["width"]-args["height"])/2 - args["center_x"], args["center_y"]),
                #    args["width"]/2
                #)
                # rectじゃなくてここだけlineにしてもよいかも
                #rect = pygame.Rect(0,0,args["width"]-args["height"],args["height"])
                #rect.center = (args["center_x"], args["center_y"])
                #pygame.draw.rect(
                #    self.screen,
                #    self.window_info["color"][1],
                #    rect
                #)

import sys

def main():
    gui=GraphicInterface("laptop.json")
    pygame.init()
    gui.begin()
    while True:
        gui.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()