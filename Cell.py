import pygame
from pygame import gfxdraw


# Constants
gap_w = 14
gap_h = 10
radius = 21

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Dictionary to store colour codings according to value in cell
colour_codings = {0: white, 1: red, 2: yellow}


class Cell:
    """
    Each cell is defined by it's row, column and value inside it
    Value = 0 if it's empty
    Value = 1 if it's filled by player 1
    Value = 2 if it's filled by player 2
    """

    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val
        self.x = (self.col + 1) * gap_w + radius * (1 + 2 * self.col)
        self.y = (self.row + 1) * gap_h + radius * (1 + 2 * self.row) + 50

    def draw(self, window):
        gfxdraw.aacircle(window, self.x, self.y, radius, colour_codings[self.val])
        gfxdraw.filled_circle(window, self.x, self.y, radius, colour_codings[self.val])

    def set_val(self, val):
        self.val = val
