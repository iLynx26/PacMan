import pygame

class Berry:
    def __init__(self, x, y, isbig, image):
        self.x = x
        self.y = y
        self.isbig = isbig
        self.image = image
        self.eaten = False
    def eat(self):
        if self.eaten:
            return(0)
        
        self.eaten = True

        if self.isbig:
            return(10)
        else:
            return(1)
            
    def draw(self, screen):
        if not self.eaten:
            screen.blit(self.image, (self.x * 20, self.y * 20))
        