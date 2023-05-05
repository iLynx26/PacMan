import pygame

class Wall:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
    
    def draw(self, screen):
        screen.blit(self.image, (self.x * 20, self.y * 20))