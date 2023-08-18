import pygame
import globals
import random
import math
import dir

class Ghost:
    def __init__(self, x, y, min_speed, max_speed):
        self.image = pygame.image.load('images/clyde.png')
        self.image = pygame.transform.scale(self.image, (globals.block_size, globals.block_size))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.speed = min_speed
        self.directions = []
        self.last_intersection = ()
        self.dir = None

    def draw(self, screen):
        screen.blit(self.image, (self.x * globals.block_size, self.y * globals.block_size))
    
    def update(self, map):
        print("-- ghost update")
        self.speed = globals.lerp_difficulty(self.min_speed, self.max_speed)
        directions = map.get_available_directions(self.x, self.y, self.min_speed)
        print(f"Current: {self.dir}; Available: {directions}; {self.directions}")
        if self.directions != directions:
            if self.dir not in directions:
                print("rounded!")
                self.x = int(self.x)
                self.y = int(self.y)
                print(self.x, self.y)
                directions = map.get_available_directions(self.x, self.y, self.min_speed)
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
    
    def set_random_direction(self):
        directions = self.directions.copy()
        if self.dir != None: 
            removable_direction = dir.get_opposite_direction(self.dir)
            if removable_direction not in directions:
                print(removable_direction)
            else:
                directions.remove(removable_direction)
        self.dir = directions[random.randint(0, len(directions)-1)]
    def get_map_coords(self):
        x_center = self.x+0.5
        y_center = self.y+0.5
        return [math.floor(x_center), math.floor(y_center)]
