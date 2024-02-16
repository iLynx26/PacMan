import pygame
import globals

class Shrub:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
    
    def draw(self, screen):
        screen.blit(self.image, (self.x * globals.block_size, self.y * globals.block_size))