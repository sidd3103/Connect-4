import pygame
from Cell import Cell

pygame.init()

WINDOW_WIDTH = 812
WINDOW_HEIGHT = 644
gap = WINDOW_WIDTH / 7

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)


class Board:
    def __init__(self, window):
        self.window = window
        self.board = [[0 for j in range(7)] for i in range(6)]
        self.cells = [[Cell(i, j, 0) for j in range(7)] for i in range(6)]

    def check_direction(self, row, col, row_vel, col_vel, player, count):
        if row >= 6 or col >= 7 or row < 0 or col < 0 or self.board[row][col] != player:
            return False

        if count == 3:
            return True

        return self.check_direction(row + row_vel, col + col_vel, row_vel, col_vel, player, count + 1)

    def check_if_win(self, row, col, player):
        return self.check_direction(row, col, 0, 1, player, 0) or \
               self.check_direction(row, col, 0, -1, player, 0) or \
               self.check_direction(row, col, 1, 0, player, 0) or \
               self.check_direction(row, col, -1, 0, player, 0) or \
               self.check_direction(row, col, 1, 1, player, 0) or \
               self.check_direction(row, col, 1, -1, player, 0) or \
               self.check_direction(row, col, -1, -1, player, 0) or \
               self.check_direction(row, col, -1, 1, player, 0)

    def draw_cells(self):
        for i in range(6):
            for j in range(7):
                self.cells[i][j].draw(self.window)

    def update(self):
        self.window.fill(black)
        self.draw_cells()
        pygame.display.update()

    def find_empty(self, col):
        for i in range(5, -1, -1):
            if self.board[i][col] == 0:
                return i
        return -1

    def play(self):
        run = True
        player = 1
        chance = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    chance = True

            if chance:
                coord = pygame.mouse.get_pos()
                column = coord[0] // 116
                row = self.find_empty(column)
                if row != -1:
                    self.board[row][column] = player
                    self.cells[row][column].setVal(player)
                    if self.check_if_win(row, column, player):
                        run = False
                    player = (player % 2) + 1
                chance = False

            self.update()


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
b = Board(window)
b.play()
pygame.quit()
