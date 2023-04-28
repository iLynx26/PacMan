import pygame
from berry import Berry
from wall import Wall

class Map:
    def __init__(self, map_def: list):
        self.images = {"berry":pygame.image.load("images/berry.png"),
                       "berry_2":pygame.image.load("images/berry_2.png"),
                       "wall":pygame.image.load("images/wall_blue.png")
                       }
        
        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], (20, 20))
            

        self.parse(map_def)

    def parse(self, map_def: list):
        x = 0
        y = 0

        objects = []

        for row in map_def:
            row_list = row.split("")
            for symbol in row_list:
                if symbol == "#":
                    objects.append(Wall(x, y))
                elif symbol == "0":
                    objects.append(Berry(x, y, False))
                elif symbol == "O":
                    objects.append(Berry(x, y, True))
                x += 1
            y += 1
        
        self.objects = objects
    
    def render(self, screen):
        screen.blit()
