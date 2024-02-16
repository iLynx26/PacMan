import pygame
import globals
from berry import Berry
from shrub import Shrub
from tree import Tree

class Map:
    def __init__(self, pacman, map_def: list):
        self.images = {"berry":pygame.image.load("images/berry.png"),
                       "berry_2":pygame.image.load("images/berry_2.png"),
                       "shrub":pygame.image.load("images/tree trunk.png"),
                       "grass":pygame.image.load("images/grass2.png"),
                       "tree":pygame.image.load("images/tree2.0.png")
                       }

        
        for key in self.images:
            height_multiplier = 1
            width_multiplier = 1
            if key == "tree":
                height_multiplier = 1
                width_multiplier = 1
            self.images[key] = pygame.transform.smoothscale(self.images[key], (globals.block_size * width_multiplier, globals.block_size * height_multiplier))
        self.berry_count = 0
        self.eaten_count = 0
        self.pacman = pacman

        self.parse(map_def)


    def parse(self, map_def: list):

        x = 0
        y = 0

        objects = []
       
        for row in map_def:
            for symbol in row:
                if symbol == "#":
                    objects.append(Shrub(x, y, self.images["shrub"]))
                elif symbol == "0":
                    self.berry_count += 1
                    objects.append(Berry(x, y, False, self.images["berry"]))
                elif symbol == "O":
                    self.berry_count += 1
                    objects.append(Berry(x, y, True, self.images["berry_2"]))
                elif symbol == "T":
                    objects.append(Tree(x, y, self.images["tree"]))
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
        if type(object) == Shrub or type(object) == Tree:
            return True
        object = self.collide(x + top_right[0], y + top_right[1])
        if type(object) == Shrub or type(object) == Tree:
            return True
        object = self.collide(x + bottom_left[0], y + bottom_left[1])
        if type(object) == Shrub or type(object) == Tree:
            return True
        object = self.collide(x + bottom_right[0], y + bottom_right[1])
        if type(object) == Shrub or type(object) == Tree:
            return True
        if object is None:
            return False
        elif type(object) == Shrub or type(object) == Tree:
            return True
        else:
            return False
    
    def collide_wall_ghost(self, x, y, dir, slop, ignore_shrubs = False):
        top_left = [slop, slop]
        top_right = [1-slop, slop]
        bottom_left = [slop, 1-slop]
        bottom_right = [1-slop, 1-slop]

        
        object = self.collide(x + top_left[0], y + top_left[1],)
        if (type(object) == Shrub and ignore_shrubs == False) or type(object) == Tree:
            return True
        object = self.collide(x + top_right[0], y + top_right[1])

        if (type(object) == Shrub and ignore_shrubs == False) or type(object) == Tree:
            return True
        object = self.collide(x + bottom_left[0], y + bottom_left[1])
        if (type(object) == Shrub and ignore_shrubs == False) or type(object) == Tree:
            return True
        object = self.collide(x + bottom_right[0], y + bottom_right[1])
        if (type(object) == Shrub and ignore_shrubs == False) or type(object) == Tree:
            return True
        if object is None:
            return False
        elif (type(object) == Shrub and ignore_shrubs == False) or type(object) == Tree:
            return True
        else:
            return False


    def get_available_directions(self, x, y, speed, slop, ignore_shrubs = False):
        directions = []
        if not self.collide_wall_ghost(x, y-speed, "", slop, ignore_shrubs):
            directions.append("up")
        if not self.collide_wall_ghost(x, y+speed, "", slop, ignore_shrubs):
            directions.append("down")
        if not self.collide_wall_ghost(x-speed, y, "", slop, ignore_shrubs):
            directions.append("left")
        if not self.collide_wall_ghost(x+speed, y, "", slop, ignore_shrubs):
            directions.append("right")
        return directions
    
    #difficulty is a number from 0 to 1 which decidec how quick and "smart" the ghosts are. 0 is easy, 1 is hard
    def calculate_difficulty(self):
        globals.difficulty = self.eaten_count / self.berry_count
        if globals.difficulty > 1:
            globals.difficulty = 1 #to hadle cheating
    
    def eat_berries_cheat(self):
        self.eaten_count += 20