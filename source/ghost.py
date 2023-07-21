import pygame
import globals
import random

class Ghost:
    def __init__(self, x, y, speed):
        self.image = pygame.image.load('images/clyde.png')
        self.image = pygame.transform.scale(self.image, (globals.block_size, globals.block_size))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.speed = speed
        self.directions = []

    def draw(self, screen):
        screen.blit(self.image, (self.x * globals.block_size, self.y * globals.block_size))
    
    def update(self, map):
        directions = map.get_available_directions(self.x, self.y, self.speed)
        if self.directions != directions:
            self.directions = directions
            self.dir = directions[random.randint(0, len(directions) - 1)]
        if self.dir == 'up':
            self.y -= self.speed
        elif self.dir == 'down':
            self.y += self.speed
        elif self.dir == 'left':
            self.x -= self.speed
        elif self.dir == 'right':
            self.x += self.speed
