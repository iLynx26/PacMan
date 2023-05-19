import pygame
from map import Map
import math as m
speed = 1/15

class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("images/pacman.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
    
    def draw(self, screen):
        screen.blit(self.image, (self.x * 20, self.y * 20))
    
    def move(self, map):
        if pygame.key.get_pressed()[pygame.K_UP] and not map.collide_wall(self.x, self.y-speed):
            self.y -= speed
        if pygame.key.get_pressed()[pygame.K_DOWN] and not map.collide_wall(self.x, self.y+speed):
            self.y += speed      
        if pygame.key.get_pressed()[pygame.K_LEFT] and not map.collide_wall(self.x-speed, self.y):
            self.x -= speed
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if not map.collide_wall(self.x+speed, self.y):
                self.x += speed