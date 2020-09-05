import pygame
from pygame import gfxdraw


gap_w = 14
gap_h = 10
radius = 21
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

colour_codings = {0: white, 1: red, 2: yellow}


class Cell:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val
        self.x = (self.col + 1) * gap_w + radius * (1 + 2 * self.col)
        self.y = (self.row + 1) * gap_h + radius * (1 + 2 * self.row) + 50

    def draw(self, window):
        gfxdraw.aacircle(window, self.x, self.y, radius, colour_codings[self.val])
        gfxdraw.filled_circle(window, self.x, self.y, radius, colour_codings[self.val])

    def setVal(self, val):
        self.val = val
