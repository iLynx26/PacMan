import pygame
import globals
from berry import Berry
from shrub import Shrub
from tree import Tree
from rock_edge import RockEdge

class Map:
    def __init__(self, pacman, tiled_map, fox, arctic_fox, chicken, owl):
        self.images = {"berry":pygame.image.load("images/cherry.png"),
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
        self.objects = []
        self.berry_count = 0
        self.eaten_count = 0
        self.pacman = pacman
        self.fox = fox
        self.chicken = chicken
        self.arctic_fox = arctic_fox
        self.owl = owl
        self.lastdeathtime = 0
        self.load_from_tiled(tiled_map)


    def load_from_tiled(self, tiled_map):
        self.width = tiled_map.width
        self.height = tiled_map.height
        for layer in tiled_map.layers:
            if layer.name == "walking":
                self.objects.append(self.pacman)
                self.objects.append(self.fox)
                self.objects.append(self.chicken)
                self.objects.append(self.arctic_fox)
            elif layer.name == "flying":
                self.objects.append(self.owl)
            for x, y, image in layer.tiles():
                if layer.name == "rocks":
                    self.objects.append(Tree(x, y, pygame.transform.smoothscale(image, (globals.block_size, globals.block_size))))
                elif layer.name == "trees" or layer.name == "trees bottom":
                    self.objects.append(Shrub(x, y, pygame.transform.smoothscale(image, (globals.block_size, globals.block_size))))
                elif layer.name == "berry" or layer.name == "berry bottom":
                    self.berry_count += 1
                    self.objects.append(Berry(x, y, False, pygame.transform.smoothscale(image, (globals.block_size, globals.block_size))))
                elif layer.name == "rocks no collision" or layer.name == "trees no collision":
                    self.objects.append(RockEdge(x, y, pygame.transform.smoothscale(image, (globals.block_size, globals.block_size))))
                elif layer.name == "berry big":
                    self.berry_count += 1
                    self.objects.append(Berry(x, y, True, pygame.transform.smoothscale(image, (globals.block_size, globals.block_size))))
                
    def pacmanisdead(self):
        current_time = pygame.time.get_ticks()
        if current_time < self.lastdeathtime + 3000:
            return False
        x1 = self.pacman.x
        y1 = self.pacman.y
        x2 = 0
        y2 = 0
        animals = [self.fox, self.arctic_fox, self.owl, self.chicken]
        for animal in animals:
            x2 = animal.x
            y2 = animal.y
            distance = ((x2-x1) ** 2 + (y2-y1) ** 2) ** 0.5
            if distance < 0.5:
                self.lastdeathtime = current_time
                return True
        return False



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
        
    
    def draw_rocks(self, screen):      
        for object in self.objects:
            if type(object) is RockEdge:
                object.draw(screen)


    def collide(self, x, y):
        for object in self.objects:
            if type(object) == RockEdge:
                continue
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
    