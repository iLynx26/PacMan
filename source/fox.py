import pygame
import globals
import random
import math
import dir

class Fox:
    def __init__(self, x, y, min_speed, max_speed):
        image = pygame.image.load('images/fox, woods.png')
        # self.image = pygame.transform.scale(self.image, (globals.block_size, globals.block_size))
        self.x = x
        self.y = y
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.speed = min_speed
        self.directions = []
        self.last_intersection = ()
        self.dir = None
        self.frame = 0
        self.counter = 0
        y = 0

        self.images = {}

        for direction in ["down",	"right", "left","up"]:
            self.images[direction] = []
            for number in range(0, 4):
                frame = image.subsurface((number * 64, y * 64, 64, 64))
                self.images[direction].append(pygame.transform.smoothscale(frame, (globals.block_size+14, globals.block_size+14)))
            y += 1

    def draw(self, screen):
        screen.blit(self.images[self.dir][self.frame], (self.x * globals.block_size-7, self.y * globals.block_size-7))
    
    def update(self, map):
        self.speed = globals.lerp_difficulty(self.min_speed, self.max_speed)
        directions = map.get_available_directions(self.x, self.y, self.speed)
        if self.directions != directions:
            if self.dir not in directions:
                self.x = round(self.x)
                self.y = round(self.y)
                directions = map.get_available_directions(self.x, self.y, self.speed)
            self.directions = directions
            if self.get_map_coords() != self.last_intersection:
                self.set_random_direction()
                self.last_intersection = self.get_map_coords()
        if self.dir == 'up':
            self.y -= self.speed
        elif self.dir == 'down':
            self.y += self.speed
        elif self.dir == 'left':
            self.x -= self.speed
        elif self.dir == 'right':
            self.x += self.speed

        self.animate(self.dir)
    
    def set_random_direction(self):
        directions = self.directions.copy()
        if self.dir != None: 
            removable_direction = dir.get_opposite_direction(self.dir)
            if removable_direction not in directions:
                print(removable_direction)
            else:
                directions.remove(removable_direction)
        self.animate(directions[random.randint(0, len(directions)-1)])
    def get_map_coords(self):
        x_center = self.x+0.5
        y_center = self.y+0.5
        return [math.floor(x_center), math.floor(y_center)]
    
    def animate(self, dir):
        if self.dir == dir:
            self.counter += 1
            if self.counter == 5:
                self.counter = 0
                self.frame += 1
                if self.frame > 2:
                    self.frame = 0
        else:
            self.dir = dir
            self.frame = 0
