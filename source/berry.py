import pygame

class Berry:
    def __init__(self, x, y, isbig, image):
        self.x = x
        self.y = y
        self.isbig = isbig
        self.image = image
    def eat(self):
        return(self.isbig)
    
    def draw(self, screen):
        screen.blit(self.image, (self.x * 20, self.y * 20))
        