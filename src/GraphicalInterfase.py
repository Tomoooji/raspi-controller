import pygame
import json
import os.path as path

class GraphicInterfase:
    def __init__(self,config_json):
        with open(path.join("config",config_json), "r") as config:
            self.window_info = json.load(config)
        self.screen = None
    
    def begin(self):
        self.screen = pygame.display.set_mode(self.window_info["size"])
        if "title" in self.window_info:
            pygame.dispay.set_caption(self.window_info["title"])
    
    def drawFlame(self):
        if "rect" in self.window_info:
            for args in self.window_info["rect"]:
                rect = pygame.Rect(0,0,args["width"],args["heighr"])
                rect.center = (args["center_x"], args["center_y"])
                pygame.draw.rect(
                    self.screen,
                    self.window_info["color"][0],
                    rect,
                    5
                )
        
        if "circle" in self.window_info:
            for args in self.window_info["circle"]:
                pygame.draw.circle(
                    self.screen,
                    self.window_info["color"][0],
                    (args["center_x"], args["center_y"]),
                    args["radius"]
                )
        
        if "stick" in self.window_info:
            for args in self.window_info["stick"]:
                pygame.draw.circle(
                    self.screen,
                    self.window_info["color"][1]
                    (args["center_x"],args["center_y"]),
                    args["out_radius"],
                    5
                )

        if "bar_h" in self.window_info:
            for args in self.window_info["bar"]:
                pygame.draw.circle(
                    self.screen,
                    self.window_info["color"][1],
                    ((args["width"]-args["height"])/2 + args["center_x"], args["center_y"]),
                    args["width"]/2
                )
                pygame.draw.circle(
                    self.screen,
                    self.window_info["color"][1],
                    ((args["width"]-args["height"])/2 - args["center_x"], args["center_y"]),
                    args["width"]/2
                )
                rect = pygame.Rect(0,0,args["width"]-args["height"],args["height"])
                rect.center = (args["center_x"], args["center_y"])
                pygame.draw.rect(
                    self.screen,
                    self.window_info["color"][1],
                    rect
                )
    
    