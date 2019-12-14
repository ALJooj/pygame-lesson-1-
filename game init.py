import pygame
# инициализация Pygame:
pygame.init()
# размеры окна:
size = width, height = 800, 600
screen = pygame.display.set_mode(size)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[1] * width for _ in range(height)]
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
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (x + 1, y + 1, w - 2, w - 2))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        # print(cell)
        self.on_click(cell)
        if self.width > cell[0] >= 0:
            if self.height > cell[1] >= 0:
                for i, elem in enumerate(self.board[cell[1]]):
                    if elem == self.board[cell[1]][i] == 1:
                        self.board[cell[1]][i] = 0
                    else:
                        self.board[cell[1]][i] = 1

                for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        if i == cell[1]:
                            continue
                        if j == cell[0]:
                            if self.board[i][j] == 1:
                                self.board[i][j] = 0


                            else:
                                self.board[i][j] = 1


    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x1 = (x - self.left) // self.cell_size
        y1 = (y - self.top) // self.cell_size

        return x1, y1

    def on_click(self, cell):
        # print(cell)
        pass


running = True
r = 10
v = 10  # пикселей в секунду
fps = 60
clock = pygame.time.Clock()
screen.fill((0, 0, 255))

screen2 = pygame.Surface(screen.get_size())
screen2.fill((0, 0, 255))

x1, y1, w, h = 0, 0, 0, 0
board = Board(4, 3)
board.set_view(100, 100, 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)

    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()


pygame.quit()