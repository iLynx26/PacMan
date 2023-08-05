from map import Map
from pacman import PacMan
import pygame
import scoreboard as sb
from ghost import Ghost

pygame.init()

clock = pygame.time.Clock()

(width, height) = (1280, 960)
screen = pygame.display.set_mode((width, height))

exit = False

map_list = [
    "###################",
    "#0 0 0 0 0 0 0 0 0#",
    "# ####0#####0#### #",
    "#0 0 0 # O # 0 0 0#",
    "# ####0#0#0#0#### #",
    "#0#### # # # ####0#",
    "# # 0 0 0#0 0 0 # #",
    "#0#0## ##### ##0#0#",
    "# 0 0#0 0O0 0#0 0 #",
    "#### # ##### # ####",
    "####0 0#####0 0####",
    "#### # ##### # ####",
    "####0#0 0 0 0#0####",
    "#0 0 ####O#### 0 0#",
    "# ##0 0 0 0 0 0## #",
    "#0## ####0#### ##0#",
    "# 0 0 0##O##0 0 0 #",
    "#0#### 0 0 0 ####0#",
    "# # 0 0#####0 0 # #",
    "#0#0## ##### ##0#0#",
    "# # ##0#####0## # #",
    "#O 0 0 0 0 0 0 0 O#",
    "###################"
    ]

map = Map(map_list)
map.screen = screen
pacman = PacMan(1, 2)
ghost = Ghost(6, 7, 1/15, 1/11)
#player speed is 1/15

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
	
    clock.tick(30)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    screen.fill((0,0,0))
    pacman.move(map)

    ghost.update(map)

    map.draw(screen)    
    pacman.draw(screen)
    ghost.draw(screen)

    sb.show_score(pacman.score, screen)

    pygame.display.flip()

    map.calculate_difficulty()