import pygame
from random import randint
# инициализация Pygame:
pygame.init()
# размеры окна:
size = width, height = 800, 600
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.turn = 0
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                w = self.cell_size
                pygame.draw.rect(screen, (200, 200, 200),
                                 (x, y, w, w), 1)
                if self.board[i][j] == 10:
                    pygame.draw.rect(screen, (255, 0, 0),
                                     (x + 1, y + 1, w - 2, w - 2))

                elif self.board[i][j] in range(0, 10):
                    font = pygame.font.Font(None, 30)
                    text = font.render(str(self.board[i][j]), 1, (100, 255, 100))
                    text_x = (x + 2)
                    text_y = (y + 2)
                    screen.blit(text, (text_x, text_y))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if self.width > cell[0] >= 0:
            if self.height > cell[1] >= 0:
                return cell

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x1 = (x - self.left) // self.cell_size
        y1 = (y - self.top) // self.cell_size
        return x1, y1


class Minesweeper(Board):
    def __init__(self, size, mines):
        self.turn = 0
        self.mines = mines
        self.width = size[0]
        self.height = size[1]
        self.board = [[-1] * width for _ in range(height)]
        m = self.mines
        while m != 0:
            r1 = randint(0, self.width - 1)
            r2 = randint(0, self.height - 1)
            if self.board[r2][r1] == -1:
                self.board[r2][r1] = 10
                m -= 1
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if self.width > cell[0] >= 0:
            if self.height > cell[1] >= 0:
                self.open_cell(cell)

    def open_cell(self, cell):
        n = 0
        if self.board[cell[1]][cell[0]] == 10:
            return
        for i in range(cell[1] - 1, cell[1] + 2):
            for j in range(cell[0] - 1, cell[0] + 2):
                if self.board[i][j] == 10:
                    n += 1
        self.board[cell[1]][cell[0]] = n


screen.fill((0, 0, 255))
running = True
cell_size = 50
x1, y1, w, h = 0, 0, 0, 0
minesweeper = Minesweeper((7, 7), 5)
minesweeper.set_view(100, 100, cell_size)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            minesweeper.get_click(event.pos)
    screen.fill((0, 0, 0))
    minesweeper.render()
    pygame.display.flip()

# завершение работы:
pygame.quit()