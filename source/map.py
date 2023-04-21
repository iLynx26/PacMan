import pygame
from berry import Berry
from wall import Wall

class Map:
    def __init__(self, map_def: list):
        self.parse(map_def)

    def parse(self, map_def: list):
        x = 0
        y = 0
        map_x = 0
        map_y = 0

        for row in map_def:
            row_list = row.split("")
            for symbol in row_list:
                if symbol == "#":
                    Wall()
