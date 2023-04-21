import pygame

class Berry:
    def __init__(self, x, y, isbig):
        self.x = x
        self.y = y
        self.isbig = isbig
    def eat(self):
        return(self.isbig)
        