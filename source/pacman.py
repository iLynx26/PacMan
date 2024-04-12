import pygame
import globals
from map import Map
from berry import Berry
import math as m

class PacMan:
    def __init__(self, x, y, min_speed, max_speed):
        self.x = x
        self.y = y
        self.image = pygame.image.load("images/pacman.png")
        self.image = pygame.transform.smoothscale(self.image, (globals.block_size, globals.block_size))
        self.score = 0
        self.frame = 0
        self.direction = "right"
        self.images = {}
        self.counter = 0
        self.min_speed = min_speed
        self.max_speed = max_speed

        for direction in ["up", "down", "left", "right"]:
            self.images[direction] = []
            for number in range(1, 4):
                image = pygame.image.load("images/" + "raccoon-" + direction + "-" + str(number) + ".png")
                self.images[direction].append(pygame.transform.smoothscale(image, (globals.block_size, globals.block_size)))

    
    def draw(self, screen):
        screen.blit(self.images[self.direction][self.frame], (self.x * globals.block_size, self.y * globals.block_size))
    
    def move(self, map):
        speed = globals.lerp_difficulty(self.min_speed, self.max_speed)
        if pygame.key.get_pressed()[pygame.K_UP] and not map.collide_wall(self.x, self.y-speed, "up"):
            self.animate("up")
            self.y -= speed
        if pygame.key.get_pressed()[pygame.K_DOWN] and not map.collide_wall(self.x, self.y+speed, "down"):
            self.animate("down")
            self.y += speed      
        if pygame.key.get_pressed()[pygame.K_LEFT] and not map.collide_wall(self.x-speed, self.y, "left"):
            self.animate("left")
            self.x -= speed
        if pygame.key.get_pressed()[pygame.K_RIGHT] and not map.collide_wall(self.x+speed, self.y, "right"):
            self.animate("right")
            self.x += speed
        if pygame.key.get_pressed()[pygame.K_F9]:
            map.eat_berries_cheat()
        object = map.collide(self.x + 0.5, self.y + 0.5)

        if type(object) == Berry:
            score = object.eat()
            if score > 0:
                self.score += score
                map.eaten_count += 1
        


            # Where we left of and what we want to try: PacMan cell; pressing two keys at once goes into different location then it's original; right + down + heading right = down
    
    def animate(self, dir):
        if self.direction == dir:
            self.counter += 1
            if self.counter == 10:
                self.counter = 0
                self.frame += 1
                if self.frame > 2:
                    self.frame = 0
        else:
            self.direction = dir
            self.frame = 0
        