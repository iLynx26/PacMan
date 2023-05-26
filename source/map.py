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
            for symbol in row:
                if symbol == "#":
                    objects.append(Wall(x, y, self.images["wall"]))
                elif symbol == "0":
                    objects.append(Berry(x, y, False, self.images["berry"]))
                elif symbol == "O":
                    objects.append(Berry(x, y, True, self.images["berry_2"]))
                x += 1
            x = 0
            y += 1
        
        self.objects = objects
    
    def draw(self, screen):
        for object in self.objects:
            object.draw(screen)

    def collide(self, x, y):
        for object in self.objects:
            if object.x == int(x) and object.y == int(y):
                pygame.draw.circle(self.screen, (255, 255, 255), (600, 100), 5)
                return object
        return None
    
    def collide_wall(self, x, y):
        object = self.collide(x+0.99, y)
        if type(object) == Wall:
            return True
        object = self.collide(x, y+0.99)
        if type(object) == Wall:
            return True
        object = self.collide(x, y)
        if type(object) == Wall:
            return True
        object = self.collide(x+0.99, y+0.99)
        if type(object) == Wall:
            return True
        if object is None:
            return False
        elif type(object) == Wall:
            return True
        else: 
            return False