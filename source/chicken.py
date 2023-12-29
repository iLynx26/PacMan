import pygame
import globals
import random
import math
import dir

class Chicken:
    def __init__(self, x, y, min_speed, max_speed):
        image = pygame.image.load('images/chicken.png')
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
        self.prev_x = -1
        self.prev_y = -1

        self.images = {}

        for direction in ["up", "right", "down", "left"]:
            self.images[direction] = []
            for number in range(0, 3):
                frame = image.subsurface((number * 32, y * 32, 32, 32))
                self.images[direction].append(pygame.transform.smoothscale(frame, (globals.block_size+14, globals.block_size+14)))
            y += 1

    def draw(self, screen):
        screen.blit(self.images[self.dir][self.frame], (self.x * globals.block_size-7, self.y * globals.block_size-7))
    
    def update(self, map):
        print(self.x, self.y)
        self.speed = globals.lerp_difficulty(self.min_speed, self.max_speed)
        if int(self.prev_x) != int(self.x) or int(self.prev_y) != int(self.y):
            directions = map.get_available_directions(round(self.x), round(self.y), self.speed, 0.01)
            if self.directions != directions:
                if self.dir not in directions:
                    print("self.dir not in directions")
                    self.x = round(self.x)
                    self.y = round(self.y)
                    directions = map.get_available_directions(self.x, self.y, self.speed, 0.01)
                self.directions = directions
                if self.get_map_coords() != self.last_intersection:
                    self.set_direction(map)
                    self.last_intersection = self.get_map_coords()
        self.prev_x = self.x
        self.prev_y = self.y
        if self.dir == 'up':
            self.y -= self.speed
        elif self.dir == 'down':
            self.y += self.speed
        elif self.dir == 'left':
            self.x -= self.speed
        elif self.dir == 'right':
            self.x += self.speed

        self.animate(self.dir)
    
    def set_direction(self, map):
        #Make a local copy of the directions we found in the update function
        directions = self.directions.copy()
        if self.dir != None: 
            #Don't turn around
            removable_direction = dir.get_opposite_direction(self.dir)
            if removable_direction in directions:
                directions.remove(removable_direction)
                print(f"Removing direction {removable_direction}, dir: {self.dir}!")

        original_directions = directions.copy()

        distance = ((self.x - map.pacman.x)**2 + (self.y - map.pacman.y)**2) **0.5

        if distance > 3000:
            dist = 10
        else:
            dist = 5

        # 1 in dist chance that the chicken follows the pacman, if the pacman is below, up is removed, above the chicken - down is removed, etc.
        if random.randint(0, dist) > 0: 
            if self.y > map.pacman.y and "down" in directions:
                directions.remove('down')
            if self.y < map.pacman.y and "up" in directions:
                directions.remove('up')
            if self.x > map.pacman.x and "right" in directions:
                directions.remove('right')
            if self.x < map.pacman.x and "left" in directions:
                directions.remove('left')
            #If there are no options, then go to original(prevents crashes)
            if len(directions) == 0:
                directions = original_directions

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
