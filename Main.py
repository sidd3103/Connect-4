import Cell
import pygame

pygame.init()

window = pygame.display.set_mode((Cell.WINDOW_WIDTH, Cell.WINDOW_HEIGHT))

Cells = [[Cell.Cell(i, j, 0) for j in range(7)] for i in range(6)]

run = True
while run:
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for i in range(6):
        for j in range(7):
            Cells[i][j].draw(window)
    pygame.display.update()
