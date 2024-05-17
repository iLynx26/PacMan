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

while not exit:
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
        pacman.score = 0

    map.draw(screen)    

    sb.show_score(pacman.score, screen)

    pygame.display.flip()

    map.calculate_difficulty()