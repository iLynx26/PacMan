import pytmx
from pytmx.util_pygame import load_pygame
from map import Map
from pacman import PacMan
import pygame
import scoreboard as sb
from fox import Fox
from arctic_fox import ArcticFox
from chicken import Chicken
from owl import Owl

pygame.init()

clock = pygame.time.Clock()

(width, height) = (1280, 960)
screen = pygame.display.set_mode((width, height))

exit = False

pacman = PacMan(2, 1, 1/15, 1/10)
tiled_map = load_pygame('tiled/level.tmx')
fox = Fox(6, 7, 1/15, 1/8)
arctic_fox = ArcticFox(12, 7, 1/16, 1/8)
chicken = Chicken(2, 21, 1/18, 1/11)
owl = Owl(16, 21, 1/16, 1/9)
map = Map(pacman, tiled_map, fox, arctic_fox, chicken, owl)
map.screen = screen
#player speed is 1/15
gameover = False

while not exit and not gameover:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
	
    clock.tick(30)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    screen.fill((0,0,0))
    pacman.move(map)

    fox.update(map)
    arctic_fox.update(map)
    chicken.update(map)
    owl.update(map)

    if map.pacmanisdead():
        if pacman.lives != 1:
            pacman.score = 0
        pacman.lives -= 1
        if pacman.lives == 0:
            gameover = True
    
    if pacman.score == 15100:
        gameover = True

    if pygame.key.get_pressed()[pygame.K_F10]:
        gameover = True
    if pygame.key.get_pressed()[pygame.K_F11]:
        gameover = True
        pacman.score = 15100

    map.draw(screen)    

    sb.show_score(pacman.score, screen)

    pygame.display.flip()

    map.calculate_difficulty()

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    
    clock.tick(30)
    if pacman.score != 15100:
        font = pygame.font.Font("images/Pixel_Bubbles.ttf", 42)
        text = font.render(f"You esaped the forest!", True, (212, 212, 20))
        text_rect = text.get_rect()
        text_rect.topleft = 10, 180
        screen.blit(text, text_rect)
        text = font.render(f"You had {pacman.score} points.", True, (212, 212, 20))
        text_rect = text.get_rect()
        text_rect.topleft = 10, 230
        screen.blit(text, text_rect)
    else:
        font = pygame.font.Font("images/Pixel_Bubbles.ttf", 40)
        text = font.render(f"You got enough berries", True, (212, 212, 20))
        text_rect = text.get_rect()
        text_rect.topleft = 10, 180
        screen.blit(text, text_rect)
        text = font.render(f"to feed your family! YAY!", True, (212, 212, 20))
        text_rect = text.get_rect()
        text_rect.topleft = 10, 230
        screen.blit(text, text_rect)
    
    pygame.display.flip()

