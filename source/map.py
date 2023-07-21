import pygame
import globals
from berry import Berry
from wall import Wall

class Map:
    def __init__(self, map_def: list):
        self.images = {"berry":pygame.image.load("images/berry.png"),
                       "berry_2":pygame.image.load("images/berry_2.png"),
                       "wall":pygame.image.load("images/wall_blue.png")
                       }

        for key in self.images:
            self.images[key] = pygame.transform.smoothscale(self.images[key], (globals.block_size, globals.block_size))


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

    def collide_wall(self, x, y, dir):
        top_left = [0.1, 0.1]
        top_right = [0.9, 0.1]
        bottom_left = [0.1, 0.9]
        bottom_right = [0.9, 0.9]

        if dir == "up":
            top_left[1] = 0
            top_right[1] = 0
        if dir == "down":
            bottom_left[1] = 0.99
            bottom_right[1] = 0.99
        if dir == "left":
            top_left[0] = 0
            bottom_left[0] = 0
        if dir == "right":
            top_right[0] = 0.99
            bottom_right[0] = 0.99
        if dir == "":
            top_left = [0.01,0.01]
            top_right = [0.99,0.01]
            bottom_left = [0.01,0.99]
            bottom_right = [0.99,0.99]

        object = self.collide(x + top_left[0], y + top_left[1],)
        if type(object) == Wall:
            return True
        object = self.collide(x + top_right[0], y + top_right[1])
        if type(object) == Wall:
            return True
        object = self.collide(x + bottom_left[0], y + bottom_left[1])
        if type(object) == Wall:
            return True
        object = self.collide(x + bottom_right[0], y + bottom_right[1])
        if type(object) == Wall:
            return True
        if object is None:
            return False
        elif type(object) == Wall:
            return True
        else:
            return False

    def get_available_directions(self, x, y, speed):
        directions = []
        if not self.collide_wall(x, y-speed, ""):
            directions.append("up")
        if not self.collide_wall(x, y+speed, ""):
            directions.append("down")
        if not self.collide_wall(x-speed, y, ""):
            directions.append("left")
        if not self.collide_wall(x+speed, y, ""):
            directions.append("right")

        return directions