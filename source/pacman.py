import pygame
from map import Map
from berry import Berry
import math as m
speed = 1/15

class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("images/pacman.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.score = 0
    
    def draw(self, screen):
        screen.blit(self.image, (self.x * 20, self.y * 20))
    
    def move(self, map):
        if pygame.key.get_pressed()[pygame.K_UP] and not map.collide_wall(self.x, self.y-speed, "up"):
            self.y -= speed
        if pygame.key.get_pressed()[pygame.K_DOWN] and not map.collide_wall(self.x, self.y+speed, "down"):
            self.y += speed      
        if pygame.key.get_pressed()[pygame.K_LEFT] and not map.collide_wall(self.x-speed, self.y, "left"):
            self.x -= speed
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if not map.collide_wall(self.x+speed, self.y, "right"):
                self.x += speed
        object = map.collide(self.x + 0.5, self.y + 0.5)
        if type(object) == Berry:
            self.score += object.eat()

            # Where we left of and what we want to try: PacMan cell; pressing two keys at once goes into different location then it's original; right + down + heading right = down