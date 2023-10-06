import pygame
import globals
from berry import Berry
from wall import Wall

class Map:
    def __init__(self, map_def: list):
        self.images = {"berry":pygame.image.load("images/berry.png"),
                       "berry_2":pygame.image.load("images/berry_2.png"),
                       "wall":pygame.image.load("images/wall_blue.png"),
                       "grass":pygame.image.load("images/grass2.png")
                       }

        for key in self.images:
            self.images[key] = pygame.transform.smoothscale(self.images[key], (globals.block_size, globals.block_size))
        self.berry_count = 0
        self.eaten_count = 0

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
                    self.berry_count += 1
                    objects.append(Berry(x, y, False, self.images["berry"]))
                elif symbol == "O":
                    self.berry_count += 1
                    objects.append(Berry(x, y, True, self.images["berry_2"]))
                x += 1
            self.width = x
            x = 0
            y += 1

        self.height = y

        self.objects = objects

    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                screen.blit(self.images["grass"], (x*globals.block_size, y*globals.block_size))            
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
            top_left = [0.1,0.1]
            top_right = [0.9,0.1]
            bottom_left = [0.1,0.9]
            bottom_right = [0.9,0.9]

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
    
    def collide_wall_fox(self, x, y, dir):
        top_left = [0.01, 0.01]
        top_right = [0.99, 0.01]
        bottom_left = [0.01, 0.99]
        bottom_right = [0.99, 0.99]

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
        if not self.collide_wall_fox(x, y-speed, ""):
            directions.append("up")
        if not self.collide_wall_fox(x, y+speed, ""):
            directions.append("down")
        if not self.collide_wall_fox(x-speed, y, ""):
            directions.append("left")
        if not self.collide_wall_fox(x+speed, y, ""):
            directions.append("right")
        return directions
    
    def get_available_directions_arctic(self, x, y, speed, quadrant):
        min_width = 0
        min_height = 0
        max_width = self.width
        max_height = self.height

        if quadrant == 0:
            max_width = self.width/2
            max_height = self.height/2
        if quadrant == 1:
            min_width = self.width/2
            max_height = self.height/2
        if quadrant == 2:
            min_height = self.height/2
            max_width = self.width/2
        if quadrant == 3:
            min_height = self.height/2
            min_width = self.width/2

        directions = []
        if not self.collide_wall_fox(x, y-speed, "") and y-speed > min_height:
            directions.append("up")
        if not self.collide_wall_fox(x, y+speed, "") and y+speed < max_height:
            directions.append("down")
        if not self.collide_wall_fox(x-speed, y, "") and x-speed > min_width:
            directions.append("left")
        if not self.collide_wall_fox(x+speed, y, "") and x+speed < max_width:
            directions.append("right")
        return directions
    
    def calculate_difficulty(self):
        globals.difficulty = self.eaten_count / self.berry_count
        if globals.difficulty > 1:
            globals.difficulty = 1 #to hadle cheating
    
    def eat_berries_cheat(self):
        self.eaten_count += 20