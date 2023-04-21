from map import Map
import pygame

pygame.init()

block_size = 20

clock = pygame.time.Clock()

(width, height) = (640, 480)
screen = pygame.display.set_mode((width, height))

exit = False

map_list = ["###################\n",
"#0 0 0 0 0 0 0 0 0#\n",
"# ####0#####0#### #\n",
"#0 0 0 # O # 0 0 0#\n",
"# ####0#0#0#0#### #\n",
"#0####C# # #I####0#\n",
"# # 0 0 0#0 0 0 # #\n",
"#0#0## ##### ##0#0#\n",
"# 0 0#0 0O0 0#0 0 #\n",
"#### # ##### # ####\n",
"####0 0#####0 0####\n",
"#### # ##### # ####\n",
"####0#0 0 0 0#0####\n",
"#0 0 ####O#### 0 0#\n",
"# ##0 0 0 0 0 0## #\n",
"#0## ####0#### ##0#\n",
"# 0 0 0##O##0 0 0 #\n",
"#0####B0 0 0 ####0#\n",
"# # 0 0#####0 0 # #\n",
"#0#0## ##### ##0#0#\n",
"# # ##0#####0## # #\n",
"#O 0 0 0 0 0 0 0 O#\n",
"###################\n"]

map = Map(map_list)

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
	
    clock.tick(30)

    pygame.display.flip()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    pygame.display.update()