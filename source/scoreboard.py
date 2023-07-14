import pygame
import globals

def show_score(score, screen):
    font = pygame.font.Font("images/Pixel_Bubbles.ttf", 30)
    text = font.render("Score: " + str(score), True, (20, 20, 212))
    text_rect = text.get_rect()
    text_rect.topleft = (globals.block_size * 20, 10)
    screen.blit(text, text_rect)
