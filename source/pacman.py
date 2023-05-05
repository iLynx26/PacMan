import pygame

class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("images/pacman.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
    
    def draw(self, screen):
        screen.blit(self.image, (self.x * 20, self.y * 20))
    
    def move(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.y -= 0.125
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.y += 0.125      
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.x -= 0.125
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.x += 0.125
    