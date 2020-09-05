import pygame
from Cell import Cell
from Cell import colour_codings
from Cell import gap_w
from Cell import radius
from pygame import gfxdraw

pygame.init()

# Some constants
instruction_bar_height = 120
gap_above = 50
WINDOW_WIDTH = 406
BOARD_HEIGHT = 322 + gap_above
WINDOW_HEIGHT = BOARD_HEIGHT + instruction_bar_height
gap = 58

# Colours
purple = (90, 24, 154)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Fonts
font1 = pygame.font.SysFont('comicsans', 25)
font2 = pygame.font.SysFont('comicsans', 45)


class Board:
    def __init__(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Connect-4")
        rect = pygame.Rect(0, 0, WINDOW_WIDTH, BOARD_HEIGHT)
        self.subsurface = self.window.subsurface(rect)
        self.board = [[0 for j in range(7)] for i in range(6)]
        self.cells = [[Cell(i, j, 0) for j in range(7)] for i in range(6)]

    def check_direction(self, row, col, row_vel, col_vel, player, count):
        """
        Tail recursive method to check if player wins from board[row][col] moving in direction (row_vel, col_vel)
        :param row: row
        :param col: column
        :param row_vel: direction of row movement (either 0,+1,-1)
        :param col_vel: direction of column movement (either 0,+1,-1)
        :param player: player
        :return: bool
        """
        if row >= 6 or col >= 7 or row < 0 or col < 0 or self.board[row][col] != player:
            return False

        if count == 3:
            return True

        return self.check_direction(row + row_vel, col + col_vel, row_vel, col_vel, player, count + 1)

    def check_if_win(self, row, col, player):
        """
        Method to check if player wins from board[row][col]
        :param row: row
        :param col: column
        :param player: player
        :return: bool
        """
        return self.check_direction(row, col, 0, 1, player, 0) or \
            self.check_direction(row, col, 0, -1, player, 0) or \
            self.check_direction(row, col, 1, 0, player, 0) or \
            self.check_direction(row, col, -1, 0, player, 0) or \
            self.check_direction(row, col, 1, 1, player, 0) or \
            self.check_direction(row, col, 1, -1, player, 0) or \
            self.check_direction(row, col, -1, -1, player, 0) or \
            self.check_direction(row, col, -1, 1, player, 0)

    def draw_cells(self):
        """
        Method to draw each cell
        :return: None
        """
        for i in range(6):
            for j in range(7):
                self.cells[i][j].draw(self.window)

    def update(self, player, win):
        """
        Method to update the game board
        :param player: which player's turn
        :param win: if player won
        :return:
        """
        self.window.fill(white)
        self.subsurface.fill(purple)
        self.draw_cells()
        if not win:
            c = pygame.mouse.get_pos()[0] // gap
            x = (c + 1) * gap_w + radius * (1 + 2 * c)
            y = 30
            gfxdraw.aacircle(self.window, x, y, radius, colour_codings[player])
            gfxdraw.filled_circle(self.window, x, y, radius, colour_codings[player])

    def find_empty(self, col):
        """
        Find empty position in column
        :param col: column
        :return: int
        """
        for i in range(5, -1, -1):
            if self.board[i][col] == 0:
                return i
        return -1

    def invalid_move_message(self):
        """
        Method to blit invalid move error on screen
        :return: None
        """
        m1 = font2.render("Invalid move. Try again.", True, black)
        self.window.blit(m1, (10, BOARD_HEIGHT + 20))

    def instructions(self, player):
        """
        Method to blit instructions on screen
        :param player: player
        :return: None
        """
        m1 = font2.render("Player {}'s turn.".format(player), True, black)
        self.window.blit(m1, (10, BOARD_HEIGHT + 20))
        m2 = font2.render("Press R to reset.", True, black)
        self.window.blit(m2, (10, BOARD_HEIGHT + 60))

    def win_message(self, player):
        """
        Method to blit win message on screen
        :param player: player
        :return: None
        """
        m1 = font2.render("Player {} wins the game".format(player), True, black)
        self.window.blit(m1, (10, BOARD_HEIGHT + 30))

    def play(self):
        """
        Method to start the game
        :return: None
        """
        run = True
        player = 1
        chance = False
        reset = False
        win = False
        invalid_move = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN and not win:
                    chance = True

                if event.type == pygame.KEYDOWN:
                    e = event.key
                    reset = (e == pygame.K_r)

            if reset:
                self.board = [[0 for j in range(7)] for i in range(6)]
                self.cells = [[Cell(i, j, 0) for j in range(7)] for i in range(6)]
                player = 1
                reset = False
                win = False
                continue

            if chance:
                coord = pygame.mouse.get_pos()
                column = coord[0] // gap
                row = self.find_empty(column)
                if row != -1:
                    self.board[row][column] = player
                    self.cells[row][column].setVal(player)
                    if self.check_if_win(row, column, player):
                        win = True
                    else:
                        player = (player % 2) + 1
                    invalid_move = False
                else:
                    invalid_move = True
                chance = False

            self.update(player, win)
            if invalid_move:
                self.invalid_move_message()
            elif win:
                self.win_message(player)
            else:
                self.instructions(player)
            pygame.display.update()
